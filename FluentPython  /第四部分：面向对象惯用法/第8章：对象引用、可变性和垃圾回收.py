# 8.1 对象不是盒子

"""
如果把变量想象为盒子，那么无法解释 Python 中的赋值，应该把变量视作便利贴

"""

# 8.2 标识、相等性和别名

"""
每个变量都有标识、类型和值。对象一旦创建，它的标识绝不会变；你可以把标识理解为对象在内存中的地址。
is 运算符比较两个对象的标识； id() 函数返回对象标识的整数表示


== 运算符比较两个对象的值（对象中保存的数据），而 is 比较对象的标识。
is 运算符比 == 速度快，因为它不能重载，所以 python 不用寻找并调用特殊方法，而是直接比较两个整数ID。
而a==b 是语法糖，等同于 a.__eq__(b)。 继承自 object 的 __eq__方法比较两个对象的ID，结果于is一样。


元组的不可变性其实是指 tuple 数据结构的物理内容（即保存的引用）不可变，与引用的对象无关。
"""

# 8.3 默认做浅复制

"""
构造方法或[:] 做的是浅复制（即复制了最外层容器，副本中的元素是原容器中元素的引用）。如果所有元素都是不可变的，那么这样没有问题
还能节省内存。但是，如果有可变的元素，可能会导致意想不到的问题。

深复制（即副本不共享内部对象的引用）。copy模块提供的 deepcopy 和 copy函数能为任意函数对象做深复制和浅复制
"""

# 8.4 函数的参数作为引用时

"""
Python 唯一支持的参数传递模式时共享传参

不要使用可变类型作为参数的默认值


"""


class HauntedBus:
    """备受幽灵乘客折磨的校车"""

    def __init__(self, passengers=[]):
        self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


bus1 = HauntedBus(['Alice', 'Bill'])
print(bus1.passengers)
# ['Alice', 'Bill']

bus1.pick('Charlie')
bus1.drop('Alice')
print(bus1.passengers)  # 目前没有什么问题，bus1 没有出现异常
# ['Bill', 'Charlie']

bus2 = HauntedBus()  # 一开始，bus2 是空的，因此把默认的空列表赋值给self.passengers
bus2.pick('Carrie')
print(bus2.passengers)
# ['Carrie']

bus3 = HauntedBus()  # bus3 一开始也是空的，因此还是赋值默认的列表
print(bus3.passengers)  # 但是默认列表不为空 ！！！
# ['Carrie']

bus3.pick('Dave')
print(bus2.passengers)  # bus3 的Dave 出现在bus2中 ！！！
# ['Carrie', 'Dave']

print(bus2.passengers is bus3.passengers)  # 问题是，bus2.passagers 和 bus3.passengers  指代同一个列表 ！！！
# True

print(bus1.passengers)  # 但 bus1.passengers 是不同的列表
# ['Bill', 'Charlie']

"""
上述问题在于，没有指定初始乘客的HauntedBus 实例会共享同一乘客列表。
实例化HauntedBus 时，如果传入乘客，会按预期运作。但是不为 HauntedBus 指定乘客的话，奇怪的事就发生了，
这是因为self.passengers 变成了 passengers参数默认值的别名。
出现这个问题的根源是，默认值在定义函数时计算（通常在加载模块时），因此默认值变成了函数对象的属性。
因此，如果默认值是可变对象，而且修改了它的值，那么后续的函数调用都会受到影响

"""
print(dir(HauntedBus.__init__))
print(HauntedBus.__init__.__defaults__)
# (['Carrie', 'Dave'],)

print(HauntedBus.__init__.__defaults__[0] is bus2.passengers)
# True

"""
可变默认值导致的这个问题说明了为什么通常使用 None 作为接收可变值的参数的默认值

"""

## 防御可变参数

"""
如果定义的函数接收可变参数，应该谨慎考虑调用方是否期望修改传入的参数

"""


class TwilightBus:
    """让乘客销声匿迹的校车"""

    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


basketball_team = ['Sue', 'Tina', "Maya", 'Diana', 'Pat']
bus = TwilightBus(basketball_team)
bus.drop('Tina')
bus.drop('Pat')
print(basketball_team)
# ['Sue', 'Maya', 'Diana']
