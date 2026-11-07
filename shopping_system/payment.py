# -*- coding: utf-8 -*-
"""Payment 抽象类及其五个子类 —— 对应 A1-4 类图中的泛化结构。

        Payment (abstract)
            ▲
   ┌────┬───┴──┬────────┬──────┐
 Credit Cash WireTransfer AliPay WeixinPay
"""
from abc import ABC, abstractmethod


class Payment(ABC):
    """支付抽象类：对应类图中的 Payment，属性 - amount : Money。"""

    def __init__(self, amount: float):
        if amount < 0:
            raise ValueError("支付金额不能为负")
        self._amount = amount

    @property
    def amount(self) -> float:
        return self._amount

    @abstractmethod
    def pay(self) -> bool:
        """执行支付，返回是否成功。由五个子类各自实现，体现多态。"""

    def describe(self) -> str:
        return f"{type(self).__name__}：￥{self._amount:.2f}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(amount={self._amount})"


class Credit(Payment):
    """信用卡支付：- number : String, - type : String, - expireDate : Date"""

    def __init__(self, amount: float, number: str, type_: str, expire_date: str):
        super().__init__(amount)
        self._number = number
        self._type = type_
        self._expire_date = expire_date

    @property
    def number(self) -> str:
        return self._number

    @property
    def type(self) -> str:
        return self._type

    @property
    def expire_date(self) -> str:
        return self._expire_date

    def pay(self) -> bool:
        # 真实场景：调用银行网关；此处只校验必填项
        return bool(self._number and self._type and self._expire_date)

    def describe(self) -> str:
        masked = self._number[-4:].rjust(len(self._number), "*")
        return f"信用卡 {masked}（{self._type}，有效期至 {self._expire_date}）￥{self._amount:.2f}"


class Cash(Payment):
    """现金支付：- cashTendered : Money"""

    def __init__(self, amount: float, cash_tendered: float):
        super().__init__(amount)
        self._cash_tendered = cash_tendered

    @property
    def cash_tendered(self) -> float:
        return self._cash_tendered

    @property
    def change(self) -> float:
        """找零，实现层面的补充操作。"""
        return round(self._cash_tendered - self._amount, 2)

    def pay(self) -> bool:
        return self._cash_tendered >= self._amount

    def describe(self) -> str:
        return f"现金（实收 ￥{self._cash_tendered:.2f}，找零 ￥{self.change:.2f}）"


class WireTransfer(Payment):
    """在线转账：- bankID : String, - bankName : String"""

    def __init__(self, amount: float, bank_id: str, bank_name: str):
        super().__init__(amount)
        self._bank_id = bank_id
        self._bank_name = bank_name

    @property
    def bank_id(self) -> str:
        return self._bank_id

    @property
    def bank_name(self) -> str:
        return self._bank_name

    def pay(self) -> bool:
        return bool(self._bank_id and self._bank_name)

    def describe(self) -> str:
        return f"在线转账（{self._bank_name}，账号 {self._bank_id}）￥{self._amount:.2f}"


class AliPay(Payment):
    """支付宝支付：- number : String"""

    def __init__(self, amount: float, number: str):
        super().__init__(amount)
        self._number = number

    @property
    def number(self) -> str:
        return self._number

    def pay(self) -> bool:
        return bool(self._number)

    def describe(self) -> str:
        return f"支付宝（{self._number}）￥{self._amount:.2f}"


class WeixinPay(Payment):
    """微信支付：- number : String"""

    def __init__(self, amount: float, number: str):
        super().__init__(amount)
        self._number = number

    @property
    def number(self) -> str:
        return self._number

    def pay(self) -> bool:
        return bool(self._number)

    def describe(self) -> str:
        return f"微信支付（{self._number}）￥{self._amount:.2f}"
