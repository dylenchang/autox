"""Role operation mapper"""

from toolbox.common.persistence.sqlmodel_impl import SqlModelMapper
from toolbox.starter.system.model.role_do import RoleDO


class RoleMapper(SqlModelMapper[RoleDO]):
    pass


roleMapper = RoleMapper(RoleDO)
