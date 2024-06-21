"""Goods domain service impl"""
import io

from toolbox.common.service.impl.service_impl import ServiceImpl
from toolbox.common.util.file import generate_playbook_paths
from toolbox.starter.system.mapper.goods_mapper import GoodsMapper
from toolbox.starter.system.model.goods_do import GoodsDO
from toolbox.starter.system.schema.goods_schema import RedisDeployCmd
from toolbox.starter.system.service.goods_service import GoodsService


class GoodsServiceImpl(ServiceImpl[GoodsMapper, GoodsDO], GoodsService):
    def __init__(self, mapper: GoodsMapper):
        """
        Initialize the UserServiceImpl instance.

        Args:
            mapper (GoodsMapper): The UserMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def redis_deploy(self, redisDeployCmd: RedisDeployCmd):
        goods_record: GoodsDO = await self.mapper.select_record_by_id(id=redisDeployCmd.goods_id)
        binary_data = goods_record.data
        zip_file_object = io.BytesIO(binary_data)
        temp_dir, inventory_file_path, entry_file_path, global_var_file_path, role_names = generate_playbook_paths(zip_file_object)


