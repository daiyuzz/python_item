# -*- coding: utf-8 -*-
# @Time    : 2021/6/12 下午9:10
# @Author  : daiyu
# @File    : 创建型模式-建造者模式.py
# @Software: PyCharm


# 主餐
class Burger():
    name = ""
    price = 0.0

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price

    def getName(self):
        return self.name


class CheeseBurger(Burger):
    def __init__(self):
        self.name = "cheese burger"
        self.price = 10.0


class spicyChickenBurger(Burger):
    def __init__(self):
        self.name = "spicy chicken burger"
        self.price = 15.0


# 小食
class Snack():
    name = ""
    price = 0.0
    type = "SNACK"

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price

    def getName(self):
        return self.name


class chips(Snack):
    def __init__(self):
        self.name = "chips"
        self.price = 6.0


class chickenWings(Snack):
    def __init__(self):
        self.name = "chicken wings"
        self.price = 12.0


# 饮料

class Beverage():
    name = ""
    price = 0.0
    type = "BEVERAGE"

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price

    def getName(self):
        return self.name


class coke(Beverage):
    def __init__(self):
        self.name = "coke"
        self.price = 4.0


class milk(Beverage):
    def __init__(self):
        self.name = "milk"
        self.price = 5.0


# 最终，我们是要建造一个订单，因而，需要一个订单类。假设，一个订单，包括一份主食，一份小食，一种饮料。（省略异常判断）

class order():
    burger = ""
    snack = ""
    beverage = ""

    def __init__(self, orderBuilder):
        self.burger = orderBuilder.bBurger
        self.snack = orderBuilder.bSnack
        self.beverage = orderBuilder.bBeverage

    def show(self):
        print("Burger:%s" % self.burger.getName())
        print("Snack:%s" % self.snack.getName())
        print("Beverage:%s" % self.beverage.getName())


# 代码中的orderBuilder就是建造者模式中所谓的“建造者”了

class orderBuilder():
    bBurger = ''
    bSnack = ''
    bBeverage = ''

    def addBurger(self, xBurger):
        self.bBurger = xBurger

    def addSnack(self, xSnack):
        self.bSnack = xSnack

    def addBeverage(self, xBeverage):
        self.bBeverage = xBeverage

    def build(self):
        return order(self)


# Director类
class orderDirector():
    order_builder = ''

    def __init__(self, order_builder):
        self.order_builder = order_builder

    def createOrder(self, burger, snack, beverage):
        self.order_builder.addBurger(burger)
        self.order_builder.addSnack(snack)
        self.order_builder.addBeverage(beverage)
        return self.order_builder.build()


# 在场景中如下去实现订单的生成
if __name__ == '__main__':
    # order_builder = orderBuilder()
    # order_builder.addBurger(spicyChickenBurger())
    # order_builder.addSnack(chips())
    # order_builder.addBeverage(milk())
    # order_1 = order_builder.build()
    # order_1.show()
    order_director = orderDirector(orderBuilder())
    order_1 = order_director.createOrder(spicyChickenBurger(),chips(),milk())
    order_1.show()