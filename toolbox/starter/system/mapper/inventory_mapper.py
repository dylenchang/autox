"""Inventory operation mapper"""

from toolbox.common.persistence.sqlmodel_impl import SqlModelMapper
from toolbox.starter.system.model.inventory_do import InventoryDO


class InventoryMapper(SqlModelMapper[InventoryDO]):
    pass


inventoryMapper = InventoryMapper(InventoryDO)
