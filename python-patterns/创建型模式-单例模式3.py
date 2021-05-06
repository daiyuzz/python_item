# -*- coding: utf-8 -*-
# @Time    : 2021/5/6 下午10:20
# @Author  : daiyu
# @File    : 创建型模式-单例模式3.py
# @Software: PyCharm

# 方法3：本质上是方法2的升级（或者说高级版）
# 使用 _metaclass_(元类）的高级python用法

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class MyClass(object):
    __metaclass__ = Singleton


one = MyClass()
two = MyClass()

two.a = 3
print(one.a)
