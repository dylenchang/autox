"""Service factory to produces required services"""

from typing import Optional

from toolbox.starter.system.mapper.goods_mapper import goodsMapper
from toolbox.starter.system.mapper.inventory_mapper import inventoryMapper
from toolbox.starter.system.mapper.user_mapper import userMapper
from toolbox.starter.system.service.goods_service import GoodsService

from toolbox.starter.system.service.bare_metal_service import BareMetalService
from toolbox.starter.system.service.impl.bare_metal_service_impl import (
    BareMetalServiceImpl,
)
from toolbox.starter.system.service.impl.goods_service_impl import GoodsServiceImpl
from toolbox.starter.system.service.impl.inventory_service_impl import (
    InventoryServiceImpl,
)
from toolbox.starter.system.service.impl.user_service_impl import UserServiceImpl
from toolbox.starter.system.service.inventory_service import InventoryService
from toolbox.starter.system.service.user_service import UserService

_singleton_user_service_instance: Optional[UserService] = None
_singleton_inventory_service_instance: Optional[InventoryService] = None
_singleton_goods_service_instance: Optional[GoodsService] = None
_singleton_bare_metal_service_instance: Optional[BareMetalService] = None


def get_user_service(service_name: str = "default") -> UserService:
    """
    Return an instance of the UserService implementation.

    Returns:
        UserService: An instance of the UserServiceImpl class.
    """
    global _singleton_user_service_instance
    if service_name == "default":
        if _singleton_user_service_instance is None:
            _singleton_user_service_instance = UserServiceImpl(mapper=userMapper)
        return _singleton_user_service_instance
    else:
        raise ValueError(f"Unknown service name: {service_name}")


def get_inventory_service(service_name: str = "default") -> InventoryService:
    """
    Return an instance of the InventoryService implementation.

    Returns:
        InventoryService: An instance of the InventoryServiceImpl class.
    """
    global _singleton_inventory_service_instance
    if service_name == "default":
        if _singleton_inventory_service_instance is None:
            _singleton_inventory_service_instance = InventoryServiceImpl(
                mapper=inventoryMapper
            )
        return _singleton_inventory_service_instance
    else:
        raise ValueError(f"Unknown service name: {service_name}")


def get_goods_service(service_name: str = "default") -> GoodsService:
    """
    Return an instance of the GoodsService implementation.

    Returns:
        GoodsService: An instance of the GoodsServiceImpl class.
    """
    global _singleton_goods_service_instance
    if service_name == "default":
        if _singleton_goods_service_instance is None:
            _singleton_goods_service_instance = GoodsServiceImpl(mapper=goodsMapper)
        return _singleton_goods_service_instance
    else:
        raise ValueError(f"Unknown service name: {service_name}")


def get_bare_metal_service(service_name: str = "default") -> BareMetalService:
    """
    Return an instance of the BareMetalService implementation.

    Returns:
       BareMetalService: An instance of the BareMetalServiceImpl class.
    """
    global _singleton_bare_metal_service_instance
    if service_name == "default":
        if _singleton_bare_metal_service_instance is None:
            _singleton_bare_metal_service_instance = BareMetalServiceImpl()
        return _singleton_bare_metal_service_instance
    else:
        raise ValueError(f"Unknown service name: {service_name}")
