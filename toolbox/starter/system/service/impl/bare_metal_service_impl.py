"""BareMetal domain service impl"""

import io
import subprocess

from loguru import logger

from toolbox.common.service.impl.service_impl import ServiceImpl
from toolbox.common.util.file import generate_playbook_paths
from toolbox.starter.system.factory.session_factory import db_session
from toolbox.starter.system.mapper.goods_mapper import GoodsMapper
from toolbox.starter.system.mapper.inventory_mapper import inventoryMapper
from toolbox.starter.system.model.goods_do import GoodsDO
from toolbox.starter.system.schema.bare_metal_schema import RedisDeployCmd
from toolbox.starter.system.service.bare_metal_service import BareMetalService
from toolbox.starter.system.template.template import get_template


class BareMetalServiceImpl(ServiceImpl[GoodsMapper, GoodsDO], BareMetalService):
    def __init__(self, mapper: GoodsMapper):
        """
        Initialize the UserServiceImpl instance.

        Args:
            mapper (GoodsMapper): The UserMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def redis_deploy(self, redisDeployCmd: RedisDeployCmd):
        global temp_dir
        async with db_session() as session:
            goods_record: GoodsDO = await self.mapper.select_record_by_id(
                id=redisDeployCmd.goods_id, db_session=session
            )
        binary_data = goods_record.data
        zip_file_object = io.BytesIO(binary_data)
        try:
            (
                temp_dir,
                inventory_file_path,
                site_file_path,
                global_var_file_path,
                role_names,
            ) = generate_playbook_paths(zip_file_object)
            role_name = role_names[0]
            async with db_session() as session:
                inventoryRecords = await inventoryMapper.select_records_by_ids(
                    ids=redisDeployCmd.host_ids, db_session=session
                )
            inventory_template = get_template(role_name, "inventory.yml")
            site_template = get_template(role_name, "site.yml")
            global_template = get_template(role_name, "global.yml")
            inventory_content = inventory_template.render(hosts=inventoryRecords)
            with open(inventory_file_path, "w", encoding="utf-8") as file:
                file.write(inventory_content)
            site_content = site_template.render(role_name=role_name)
            with open(site_file_path, "w", encoding="utf-8") as file:
                file.write(site_content)
            global_content = global_template.render(
                redis_version=redisDeployCmd.version,
                redis_password=redisDeployCmd.password,
            )
            with open(global_var_file_path, "w", encoding="utf-8") as file:
                file.write(global_content)
            command = [
                "ansible-playbook",
                "-i",
                inventory_file_path,
                "-e",
                f"@{global_var_file_path}",
                site_file_path,
            ]
            logger.info(" ".join(command))
            logger.info(f"filename: {temp_dir.name}")
            return subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        finally:
            temp_dir.cleanup()
