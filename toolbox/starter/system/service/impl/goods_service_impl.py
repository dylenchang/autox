"""Goods domain service impl"""

from toolbox.common.service.impl.service_impl import ServiceImpl
from toolbox.starter.system.mapper.goods_mapper import GoodsMapper
from toolbox.starter.system.model.goods_do import GoodsDO
from toolbox.starter.system.service.goods_service import GoodsService


class GoodsServiceImpl(ServiceImpl[GoodsMapper, GoodsDO], GoodsService):
    def __init__(self, mapper: GoodsMapper):
        """
        Initialize the UserServiceImpl instance.

        Args:
            mapper (GoodsMapper): The UserMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper
