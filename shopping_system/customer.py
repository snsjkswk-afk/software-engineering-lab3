# -*- coding: utf-8 -*-
"""Customer —— 对应 A1-4 类图中的 Customer（客户）。

与 Order 是 1 : * 的关联：一个客户可有多个订单，一个订单只属于一个客户。
"""
from __future__ import annotations

from typing import List

from .order import Order


class Customer:
    """客户。

    类图属性：- name : String, - contact : String,
              - deliveryAddress : String, - active : Boolean
    """

    def __init__(self, name: str, contact: str, delivery_address: str, active: bool = True):
        self._name = name
        self._contact = contact
        self._delivery_address = delivery_address
        self._active = active
        self._orders: List[Order] = []   # 1 : * 用容器表达

    @property
    def name(self) -> str:
        return self._name

    @property
    def contact(self) -> str:
        return self._contact

    @property
    def delivery_address(self) -> str:
        return self._delivery_address

    @property
    def active(self) -> bool:
        return self._active

    @property
    def orders(self) -> List[Order]:
        return list(self._orders)

    def place_order(self, order: Order) -> Order:
        if not self._active:
            raise RuntimeError("账号未激活，不能下单")
        self._orders.append(order)
        return order

    def __repr__(self) -> str:
        return f"Customer({self._name!r}, 订单 {len(self._orders)} 笔)"
