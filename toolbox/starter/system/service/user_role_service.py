"""UserRole domain service interface"""

from abc import ABC
from typing import List

from toolbox.common.service.service import Service
from toolbox.starter.system.model.user_role_do import UserRoleDO


class UserRoleService(Service[UserRoleDO], ABC):
    async def assign_roles(
        self,
        *,
        user_id: int,
        role_ids: List[int],
    ) -> bool: ...
