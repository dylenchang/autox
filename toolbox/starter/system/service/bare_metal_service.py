"""Bare metal domain service interface"""

from abc import ABC

from toolbox.common.service.service import Service
from toolbox.starter.system.model.goods_do import GoodsDO
from toolbox.starter.system.schema.bare_metal_schema import RedisDeployCmd


class BareMetalService(Service[GoodsDO], ABC):
    async def redis_deploy(self, redisDeployCmd: RedisDeployCmd):
        pass
