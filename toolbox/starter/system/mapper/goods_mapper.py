"""Goods operation mapper"""

from toolbox.common.persistence.sqlmodel_impl import SqlModelMapper
from toolbox.starter.system.model.goods_do import GoodsDO


class GoodsMapper(SqlModelMapper[GoodsDO]):
    pass


goodsMapper = GoodsMapper(GoodsDO)
