"""Inventory domain service interface"""

from abc import ABC

from toolbox.common.service.service import Service
from toolbox.starter.system.model.inventory_do import InventoryDO


class InventoryService(Service[InventoryDO], ABC):
    async def ping_ip(self, *, ip_address: str, timeout: int = 4): ...
