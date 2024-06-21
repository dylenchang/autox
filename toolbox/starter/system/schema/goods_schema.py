"""Goods domain schema"""
from typing import List

from pydantic import BaseModel


class RedisDeployCmd(BaseModel):
    host_ids: List[int]
    goods_id: int
    version: str
    password: str