"""BareMetal domain service impl"""

import subprocess

from loguru import logger

from toolbox.common.config import configs
from toolbox.common.enum.enum import ModeEnum
from toolbox.starter.system.schema.bare_metal_schema import RedisDeployCmd, UserDeployCmd
from toolbox.starter.system.schema.base_deploy_schema import BaseDeployCmd
from toolbox.starter.system.service.bare_metal_service import BareMetalService
from toolbox.starter.system.service.impl.base_deploy_service_impl import (
    BaseDeployServiceImpl,
)
from toolbox.starter.system.template.template import get_template


class BareMetalServiceImpl(BareMetalService, BaseDeployServiceImpl):
    def __init__(self):
        super().__init__()

    async def redis_deploy(self, redisDeployCmd: RedisDeployCmd):
        global temp_dir
        try:
            baseDeployCmd = BaseDeployCmd(
                host_ids=redisDeployCmd.host_ids, goods_id=redisDeployCmd.goods_id
            )
            (
                temp_dir,
                inventory_file_path,
                site_file_path,
                global_var_file_path,
                role_name,
            ) = await self.base_deploy(baseDeployCmd)
            global_template = get_template(role_name, self.common_global_name)
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
            return subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        finally:
            if configs.mode == ModeEnum.production:
                temp_dir.cleanup()

    async def source_deploy(self, baseDeployCmd: BaseDeployCmd):
        global temp_dir
        try:
            (
                temp_dir,
                inventory_file_path,
                site_file_path,
                global_var_file_path,
                role_name,
            ) = await self.base_deploy(baseDeployCmd)
            command = [
                "ansible-playbook",
                "-i",
                inventory_file_path,
                site_file_path,
            ]
            logger.info(" ".join(command))
            return subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        finally:
            if configs.mode == ModeEnum.production:
                temp_dir.cleanup()

    async def user_deploy(self, userDeployCmd: UserDeployCmd):
        global temp_dir
        try:
            baseDeployCmd = BaseDeployCmd(
                host_ids=userDeployCmd.host_ids, goods_id=userDeployCmd.goods_id
            )
            (
                temp_dir,
                inventory_file_path,
                site_file_path,
                global_var_file_path,
                role_name,
            ) = await self.base_deploy(baseDeployCmd)
            global_template = get_template(role_name, self.common_global_name)
            global_content = global_template.render(
                user=userDeployCmd.user,
                password=userDeployCmd.password,
                group=userDeployCmd.group
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
            return subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        finally:
            if configs.mode == ModeEnum.production:
                temp_dir.cleanup()