# 主餐生成
class Burger():
    name = ""
    price = 0.0

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price

    def getName(self):
        return self.name


class cheeseBurger(Burger):
    def __init__(self):
        self.name = "cheese burger"
        self.price = 10.0


class spicyChickenBurger(Burger):
    def __init__(self):
        self.name = "spicy chicken burger"
        self.price = 15.0


# 小食生成
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


# 饮料生成
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
        self.name = 'coke'
        self.price = 4.0


class mike(Beverage):
    def __init__(self):
        self.name = "mike"
        self.price = 5.0


"""
以上的Burger，Snack，Beverage都可以认为是该快餐店的产品，由于只提供了抽象方法，我们把它们叫抽象产品类，
而cheese burger等6个由抽象产品衍生出的子类，叫做具体产品类。
接下来，”工厂“就要出现了
"""


class foodFactory():
    type = ""

    def createFood(self, foodClass):
        print(self.type, "factory priduce a instance")
        foodIns = foodClass()
        return foodIns


class burgerFactory(foodFactory):
    def __init__(self):
        self.type = "BURGER"


class snackFactory(foodFactory):
    def __init__(self):
        self.type = "SNACK"


class beverageFactory(foodFactory):
    def __init__(self):
        self.type = "BEVERAGE"


"""
同样，foodFactory为抽象的工厂类，而 burgerFactory,snackFactory,beverageFactory为具体的工厂类。
在业务场景中，工厂模式是如何”生产“产品的呢？
"""

if __name__ == '__main__':
    burger_factory = burgerFactory()
    snack_factory = snackFactory()
    beverage_factory = beverageFactory()
    cheese_burger = burger_factory.createFood(cheeseBurger)
    print(cheese_burger.getName(), cheese_burger.getPrice())
    chicken_wings = snack_factory.createFood(chickenWings)
    print(chicken_wings.getName(),chicken_wings.getPrice())
    coke_drink = beverage_factory.createFood(coke)
    print(coke_drink.getName(), coke_drink.getPrice())
