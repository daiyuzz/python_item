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
            self.passengers = []  # 这里谨慎处理，当passengers 为None时，创建一个新的空列表
        else:
            self.passengers = passengers  # 这个赋值语句把 self.passengers 变成 passengers 的别名，而后者是传给 __init__ 方法的实参

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)  # 在self.passengers 上调用 .remove() 和 .append() 方法其实会修改传给构造方法的那个列表


basketball_team = ['Sue', 'Tina', "Maya", 'Diana', 'Pat']
bus = TwilightBus(basketball_team)
bus.drop('Tina')
bus.drop('Pat')
print(basketball_team)  # 下车的学生从连球队中消失了
# ['Sue', 'Maya', 'Diana']

"""
TwlightBus 违反了设计皆苦的最佳实践，即“最少惊讶原则”。学生从校车中下车后，他的名字就从篮球名单中消失了，这确实让人惊讶

这里的问题是，校车为传给构造方法的列表创建了别名。正确的做法很简单：在__init__中，传入 passengers 参数时，应该把参数值的副本赋值给 self.passengers
如下

def __init__(self,passengers=None):
    if passengers is None:
        self.passengers = []
    else:
        self.passengers = list(passengers) # 创建 passengers 列表副本，如果不是列表，就把它转换成列表

"""

"""
除非这个方法确实想修改通过参数传入的对象，否则在类中直接把参数赋值给实例变量之前一定要三思，因为这样会为参数对象创建别名。
如果不确定，那就创建副本。

"""

# 8.5 del和垃圾回收

"""
del 语句删除名称，而不是对象。del 命令可能会导致对象被当做垃圾回收，但是仅当删除的变量保存的是对象的最后一个引用，或者无法得到对象时。
重新绑定也可能会导致对象的引用数量归零，导致对象被销毁
"""


# 8.6 弱引用
"""
正是因为有引用，对象才会在内存中存在。当对象的引用数量归零后，垃圾回收程序会把对象销毁。但是，有时需要引用对象，而不让
对象存在的时间超过所需时间。这经常在缓存中。


弱引用不会增加对象的引用数量。引用的对象称为所指对象。因此，我们说，弱引用不会妨碍所指对象被当做垃圾回收。

弱引用在缓存中很有用，因为我们不想仅因为被缓存引用着而始终保存缓存对象。

"""




# 8.8 本章小结

"""
每个Python对象都有标识、类型和值。只有对象的值会不时变化


如果两个变量指代的不可变对象具有相同的值（a==b 为True），实际上它们指代的是副本还是同一个对象的别名基本上没有什么关系，因为不可变对象的值不会
变，但是有一个例外。这里说的例外是不可变的集合，如元组 frozenset：如果不可变集合保存的是可变元素的引用，那么可变元素的值发生变化之后，不可变集合
也会随之改变。实际上这种情况不是很常见。不可变集合不变的是所含对象的标识。


变量保存的是引用，这一点对 Python 编程有很多实际的影响

- 简单的赋值不创建副本
- 对 += 或 *= 所做的增量赋值来说，如果左边的变量绑定的是不可变对象，会创建新对象；如果是可变对象，会就地修改。
- 为现有的变量赋予新值，不会修改之前绑定的变量。这叫重新绑定：现在变量绑定了其他对象。如果变量是之前那个对象的最后一个引用，对象会被当做垃圾回收
- 函数的参数以别名的形式传递，这意味着，函数可能会修改通过参数传入的可变对象。这一行为无法避免，除非在本地创建副本，或者使用不可变对象（例如，传入元组，而不是传入列表）
- 使用可变类型作为函数参数的默认值有危险，因为如果就地修改了参数，默认值也就改变了，这会影响以后使用默认值的调用



"""






