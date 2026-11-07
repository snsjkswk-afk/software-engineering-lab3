# -*- coding: utf-8 -*-
"""shopping_system —— 软件工程实验三 A1-4「简化网上购物系统」的代码实现。

类与模块的对应关系：
    Customer      customer.py
    Order         order.py
    OrderDetail   order_detail.py
    Product       product.py
    OrderStatus   order_status.py
    Payment       payment.py（含 Credit / Cash / WireTransfer / AliPay / WeixinPay）
"""

from .customer import Customer
from .order import Order
from .order_detail import OrderDetail
from .order_status import OrderStatus
from .payment import AliPay, Cash, Credit, Payment, WeixinPay, WireTransfer
from .product import Product

__all__ = [
    "Customer", "Order", "OrderDetail", "Product", "OrderStatus", "Payment",
    "Credit", "Cash", "WireTransfer", "AliPay", "WeixinPay",
]
