"""Inventory domain service interface"""

from abc import ABC

from toolbox.common.service.service import Service
from toolbox.starter.system.model.inventory_do import InventoryDO


class InventoryService(Service[InventoryDO], ABC):
    async def ping_ip(self, *, ip_address: str, timeout: int = 4): ...
    """
    Ping an IP address.

    :param ip_address: The IP address to ping.
    :param timeout: Timeout in seconds for each ping request.
    :raises PingException: If the IP address is not reachable.
    """
