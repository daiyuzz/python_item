# -*- coding: utf-8 -*-
# @Time    : 2020/11/28 下午2:23
# @Author  : daiyu
# @File    : 第6章：使用一等函数实现设计模式.py
# @Software: PyCharm


"""
《设计模式：可复用面向对象软件的基础》一书是这样概述“策略”模式
的：
定义一系列算法，把它们一一封装起来，并且使它们可以相互替
换。本模式使得算法可以独立于使用它的客户而变化



电商领域有个功能明显可以使用“策略”模式，即根据客户的属性或订单
中的商品计算折扣



假如一个网店制定了下述折扣规则。
有 1000 或以上积分的顾客，每个订单享 5% 折扣。
同一订单中，单个商品的数量达到 20 个或以上，享 10% 折扣。
订单中的不同商品达到 10 个或以上，享 7% 折扣。
简单起见，我们假定一个订单一次只能享用一个折扣。
"""

# 实现Order类，支持插入式折扣策略

from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')


class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.card = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.card)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total:{:.2f} due:{:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotion(ABC):  # 策略：抽象基类

    @abstractmethod
    def discount(self, order):
        """返回折扣金额"""


class FidelityPromo(Promotion):  # 第一个具体策略
    """积分为1000或以上的顾客提供5%折扣"""

    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0


class BulkItemPromo(Promotion):  # 第二个具体策略
    """单个商品为20个或以上时提供10%折扣"""

    def discount(self, order):
        discount = 0
        for item in order.card:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount


class LargeOrderPromo(Promotion):  # 第三个具体策略
    """订单中的不同商品达到10个或以上时提供7%折扣"""

    def discount(self, order):
        distinct_items = {item.product for item in order.card}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0


"""
我们把 Promotion 定义为抽象基类（Abstract BaseClass， ABC），这么做是为了使用 @abstractmethod装饰器
从而表明所用的模式

"""

joe = Customer('John', 0)
ann = Customer('Ann Smith', 1100)
cart = [LineItem('bababa', 4, .5), LineItem('apple', 10, 1.5), LineItem('watermellon', 5, 5.0)]
print(Order(joe, cart, FidelityPromo()))
# <Order total:42.00 due:42.00>

print(Order(ann, cart, FidelityPromo()))
# <Order total:42.00 due:39.90>

banana_cart = [LineItem('banana', 30, .5), LineItem('apple', 10, 1.5)]
print(Order(joe, banana_cart, BulkItemPromo()))
# <Order total:30.00 due:28.50>

long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]

print(Order(joe, long_order, LargeOrderPromo()))
# <Order total:10.00 due:9.30>

print(Order(joe, cart, LargeOrderPromo()))
# <Order total:42.00 due:42.00>


## 6.1.2 使用函数实现“策略”模式

from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')


class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:  # 上下文
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


def fidelity_promo(order):
    """为积分1000或以上的顾客提供5%折扣"""
    return order.total() * .05 if order.customer.fidelity >= 100 else 0


def bulk_item_promo(order):
    """单个商品为20个或以上时提供10%折扣"""
    discount = 0
    for item in order.card:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount


def large_order_promo(order):
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    distinct_items = {item.product for item in order.card}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0


joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)

cart = [LineItem('banana', 4, .5),
        LineItem('apple', 10, .5),
        LineItem('watermellon', 5, 1.5)]

print(Order(joe, cart, fidelity_promo))

# 没必要在新建订单时实例化新的促销对象，函数拿来即用


"-==========================================================================================="

# 6.1.3 选择最佳策略：简单的方式
"""
我们继续使用上述中的顾客和购物车，在此基础地上添加3个测试

"""



