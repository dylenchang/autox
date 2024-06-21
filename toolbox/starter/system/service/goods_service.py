"""Goods domain service interface"""

from abc import ABC

from toolbox.common.service.service import Service
from toolbox.starter.system.model.goods_do import GoodsDO


class GoodsService(Service[GoodsDO], ABC):
    pass
