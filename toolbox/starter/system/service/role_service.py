"""Role domain service interface"""

from abc import ABC

from toolbox.common.service.service import Service
from toolbox.starter.system.model.role_do import RoleDO


class RoleService(Service[RoleDO], ABC): ...
