# -*- coding: utf-8 -*-
"""OrderStatus —— 对应 A1-4 类图中的 «enumeration» OrderStatus。"""
from enum import Enum


class OrderStatus(Enum):
    """订单的五个状态，与类图中的枚举常量一一对应。"""

    CREATE = "CREATE"
    PAID = "PAID"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"
    CANCEL = "CANCEL"

    def __str__(self) -> str:
        return self.value
