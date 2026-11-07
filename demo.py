# -*- coding: utf-8 -*-
"""多态结算演示：对应实验报告 4.4 节的类模型。

运行：python demo.py
"""
from shopping_system import (
    AliPay, Cash, Credit, Customer, Order, OrderStatus,
    Product, WeixinPay, WireTransfer,
)


def build_order() -> Order:
    """构造一笔包含两行明细的订单，验证组合关系与金额计算。"""
    order = Order("SO20261107001")
    order.add_item(Product("机械键盘", 0.9, "87 键茶轴", 399.0), 1)
    order.add_item(Product("无线鼠标", 0.12, "2.4G 双模", 129.0), 2)
    return order


def main() -> None:
    customer = Customer("王应桐", "13800000000", "湖北省宜昌市大学路 8 号")
    order = customer.place_order(build_order())

    print("=" * 62)
    print(f"客户：{customer.name}（{customer.contact}）")
    print(f"订单：{order.order_no}　创建日期：{order.create_date}")
    for i, d in enumerate(order.details, 1):
        print(f"  {i}. {d.product.title:<6} × {d.quantity}　"
              f"小计 ￥{d.calculate_sub_total():>8.2f}　重量 {d.calculate_weight():.3f} kg")
    print(f"合计金额 ￥{order.total_amount():.2f}　总重量 {order.total_weight():.3f} kg")
    print(f"当前状态：{order.status}")

    # 多态：同一个 pay() 调用，五种支付方式各自实现
    payments = [
        Credit(order.total_amount(), "6222020200112345678", "VISA", "2029-06"),
        Cash(order.total_amount(), 700.0),
        WireTransfer(order.total_amount(), "6228****4321", "中国工商银行"),
        AliPay(order.total_amount(), "wyt@example.com"),
        WeixinPay(order.total_amount(), "wxid_wangyingtong"),
    ]

    print("-" * 62)
    print("支付方式一览（多态调用 pay()）：")
    for p in payments:
        print(f"  {p.describe():<48} -> {'成功' if p.pay() else '失败'}")

    # 正式结算使用支付宝
    ok = order.pay(payments[3])
    print("-" * 62)
    print(f"结算结果：{'成功' if ok else '失败'}　订单状态：{order.status}")

    order.ship()
    print(f"发货后状态：{order.status}")
    order.deliver()
    print(f"签收后状态：{order.status}")
    assert order.status is OrderStatus.DELIVERED

    # 业务规则校验：已发货订单不能取消
    try:
        order.cancel()
    except RuntimeError as e:
        print(f"取消订单被拒绝：{e}")

    # 组合语义：明细随订单存在，订单的 details 由订单自身创建与持有
    print("=" * 62)
    print(f"订单持有 {len(order.details)} 条明细，明细生命周期依附订单。")


if __name__ == "__main__":
    main()
