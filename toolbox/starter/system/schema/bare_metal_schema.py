"""Bare metal domain schema"""

from toolbox.starter.system.schema.base_deploy_schema import BaseDeployCmd


class RedisDeployCmd(BaseDeployCmd):
    version: str
    password: str


class UserDeployCmd(BaseDeployCmd):
    user: str
    password: str
    group: str


class JreDeployCmd(BaseDeployCmd):
    version: str


class GithubHostDeployCmd(BaseDeployCmd):
    host: str = "151.101.100.133"
    host_backup: str = "185.199.111.133"
