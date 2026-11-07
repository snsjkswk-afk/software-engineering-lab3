# -*- coding: utf-8 -*-
"""Product —— 对应 A1-4 类图中的 Product（商品项）。"""


class Product:
    """商品项。

    类图属性：- title : String, - weight : double, - description : String
    类图操作：+ getPriceForQuantity(int) : Money, + getWeight() : double
    """

    def __init__(self, title: str, weight: float, description: str = "", price: float = 0.0):
        self._title = title
        self._weight = weight
        self._description = description
        self._price = price          # 单价，类图中未列出，作为实现所需的补充属性

    @property
    def title(self) -> str:
        return self._title

    @property
    def weight(self) -> float:
        return self._weight

    @property
    def description(self) -> str:
        return self._description

    @property
    def price(self) -> float:
        return self._price

    def get_price_for_quantity(self, quantity: int) -> float:
        """按数量计算小计金额。"""
        if quantity < 0:
            raise ValueError("数量不能为负")
        return round(self._price * quantity, 2)

    def get_weight(self) -> float:
        """单件重量（kg）。"""
        return self._weight

    def __repr__(self) -> str:
        return f"Product({self._title!r}, ￥{self._price})"
