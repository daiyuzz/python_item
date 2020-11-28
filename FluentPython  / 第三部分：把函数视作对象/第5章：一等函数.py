# -*- coding: utf-8 -*-
# @Author  : daiyu
# @File    : 第5章：一等函数.py
# @Description : 
# @Time    : 2020/11/27 下午8:58


"""
在python中，函数是一等对象。编程语言理论家把“一等对象”定义为满足下述条件的程序实体：

- 在运行时创建
- 能赋值给变量或数据结构中的元素
- 能作为参数传递给函数
- 能作为函数的返回结果


人们经常将“把函数视作一等对象”简称为“一等函数”。这样说并不完美，似乎表明这个函数中的特殊群体。
在python中，所有的函数都是一等对象
"""

"================================================================================"


# 5.1 把函数视作对象

def factorial(n):
    '''returns n!'''
    return 1 if n < 2 else n * factorial(n - 1)


print(factorial(42))
# 1405006117752879898543142606244511569936384000000000

print(factorial.__doc__)
# returns n!

print(type(factorial))
# <class 'function'>

fact = factorial
print(fact)
# <function factorial at 0x7f7746bb1430>

print(fact(5))
# 120

print(map(factorial, range(11)))
# <map object at 0x7f77efd74cd0>

print(list(map(fact, range(11))))
# [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]


"======================================================================================================"
# 5.2 高阶函数

"""
接受函数为参数，或者把函数作为结果返回的函数是高阶函数
"""

"======================================================================================================="
# 5.3 匿名函数

"""
除了作为参数传给高阶函数之外，python很少使用匿名函数。由于句法上的限制，非平凡的lambda表达式要么难以阅读，要么无法写出

lambda 句法只是语法糖：与def语句一样，lambda表达式会创建函数对象。这是 Python 中几种可调用对象的一种
"""

"========================================================================================================"
# 5.4 可调用对象

"""
除了用户定义的函数，调用运算符（即()）还可以应用到其他对象上。如果想判断对象能够调用，可以使用内置的callable()函数。

Python 数据模型文档列出了7种可调用对象

用户定义的函数
    使用def语句或lambda表达式创建

内置函数
    使用 C 语言（Cpython）实现的函数，如len或 time.strftime
    
内置方法
    使用 C 语言实现的方法，如 dict.get

方法
    在类的定义体中定义的函数

类
    调用类时会运行类的 __new__方法创建一个实例，然后运行__inti__方法，初始化实例，最后把实例返回给调用方。
    因为Python没有new运算符，所有调用类相当于调用函数

类的实例
    如果类定义了 __call__ 方法，那么它的实例可以作为函数调用
    
生成器函数
    使用 yield 关键字的函数或方法。调用生成器函数返回的是生成器对象
    

Python中有各种各样的可调用类型，因此判断对象能否调用，最安全的方法是使用内置的 callable() 函数


"""

"================================================================================================"
# 5.5 用户定义的可调用类型

'''不仅 Python 函数是真正的对象，任何 Python 对象都可以表现得像函数。为此，只需要实现实例方法 __call__'''

import random


class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self, *args, **kwargs):
        return self.pick()

bingo = BingoCage(range(3))

print(bingo.pick())
# 1

print(bingo())
# 2

print(callable(bingo))
# True


