"""Bare metal domain schema"""

from toolbox.starter.system.schema.base_deploy_schema import BaseDeployCmd


class RedisDeployCmd(BaseDeployCmd):
    version: str
    password: str


class UserDeployCmd(BaseDeployCmd):
    user: str
    password: str
    group: str
