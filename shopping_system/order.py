# -*- coding: utf-8 -*-
"""Order —— 对应 A1-4 类图中的 Order（订单）。

与 OrderDetail 是 1 : * 的组合关系：明细由订单创建并持有，
订单被取消/销毁后明细不再保留，故用容器 + 工厂方法表达。
与 Payment 是 1 : 1 的关联关系。
"""
from __future__ import annotations

import datetime
from typing import List, Optional

from .order_detail import OrderDetail
from .order_status import OrderStatus
from .payment import Payment
from .product import Product


class Order:
    """订单。

    类图属性：- createDate : Date, - status : OrderStatus
    """

    def __init__(self, order_no: str = ""):
        self._order_no = order_no or f"SO{datetime.datetime.now():%Y%m%d%H%M%S}"
        self._create_date = datetime.date.today()
        self._status = OrderStatus.CREATE
        self._details: List[OrderDetail] = []   # 组合：订单持有明细
        self._payment: Optional[Payment] = None  # 关联 1 : 1，未支付时为 None

    # ---------------- 基本属性
    @property
    def order_no(self) -> str:
        return self._order_no

    @property
    def create_date(self) -> datetime.date:
        return self._create_date

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def payment(self) -> Optional[Payment]:
        return self._payment

    @property
    def details(self) -> List[OrderDetail]:
        return list(self._details)

    # ---------------- 明细维护（组合：整体负责创建部分）
    def add_item(self, product: Product, quantity: int = 1) -> OrderDetail:
        if self._status is not OrderStatus.CREATE:
            raise RuntimeError("订单已提交，不能继续添加明细")
        detail = OrderDetail(product, quantity)
        self._details.append(detail)
        return detail

    def remove_item(self, detail: OrderDetail) -> None:
        if detail in self._details:
            self._details.remove(detail)

    # ---------------- 金额与重量
    def total_amount(self) -> float:
        return round(sum(d.calculate_sub_total() for d in self._details), 2)

    def total_weight(self) -> float:
        return round(sum(d.calculate_weight() for d in self._details), 3)

    # ---------------- 状态流转
    def pay(self, payment: Payment) -> bool:
        """结算：调用多态方法，不关心具体支付方式。"""
        if self._status is not OrderStatus.CREATE:
            raise RuntimeError(f"当前状态 {self._status} 不允许支付")
        if abs(payment.amount - self.total_amount()) > 1e-6:
            raise ValueError("支付金额与订单金额不一致")
        if not payment.pay():
            return False
        self._payment = payment
        self._status = OrderStatus.PAID
        return True

    def ship(self) -> None:
        if self._status is not OrderStatus.PAID:
            raise RuntimeError("只有已支付订单才能发货")
        self._status = OrderStatus.SHIPPING

    def deliver(self) -> None:
        if self._status is not OrderStatus.SHIPPING:
            raise RuntimeError("只有配送中的订单才能确认收货")
        self._status = OrderStatus.DELIVERED

    def cancel(self) -> None:
        if self._status in (OrderStatus.SHIPPING, OrderStatus.DELIVERED):
            raise RuntimeError("已发货订单不能直接取消")
        self._status = OrderStatus.CANCEL

    def __repr__(self) -> str:
        return (f"Order({self._order_no}, {self._status}, "
                f"{len(self._details)} 项, ￥{self.total_amount():.2f})")
