"""Bare metal domain service interface"""

from abc import ABC

from toolbox.starter.system.schema.bare_metal_schema import RedisDeployCmd
from toolbox.starter.system.schema.base_deploy_schema import BaseDeployCmd
from toolbox.starter.system.service.base_deploy_service import BaseDeployService


class BareMetalService(BaseDeployService, ABC):
    async def redis_deploy(self, redisDeployCmd: RedisDeployCmd): ...

    async def source_deploy(self, baseDeployCmd: BaseDeployCmd): ...
