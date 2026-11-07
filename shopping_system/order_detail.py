# -*- coding: utf-8 -*-
"""OrderDetail —— 对应 A1-4 类图中的 OrderDetail（订单明细行）。"""
from __future__ import annotations

from .product import Product


class OrderDetail:
    """订单明细。

    类图属性：- quantity : int
    类图操作：+ calculateSubTotal() : Money, + calculateWeight() : double
    与 Product 是 * : 1 的关联（多条明细可指向同一商品）。
    """

    def __init__(self, product: Product, quantity: int = 1):
        if quantity <= 0:
            raise ValueError("明细数量必须大于 0")
        self._product = product
        self._quantity = quantity

    @property
    def product(self) -> Product:
        return self._product

    @property
    def quantity(self) -> int:
        return self._quantity

    def calculate_sub_total(self) -> float:
        """该行小计金额。"""
        return self._product.get_price_for_quantity(self._quantity)

    def calculate_weight(self) -> float:
        """该行总重量。"""
        return round(self._product.get_weight() * self._quantity, 3)

    def __repr__(self) -> str:
        return f"OrderDetail({self._product.title!r} × {self._quantity})"
