"""UserRole operation mapper"""

from toolbox.common.persistence.sqlmodel_impl import SqlModelMapper
from toolbox.starter.system.model.user_role_do import UserRoleDO


class UserRoleMapper(SqlModelMapper[UserRoleDO]):
    pass


userRoleMapper = UserRoleMapper(UserRoleDO)
