# -*- coding: utf-8 -*-
# @Time    : 2021/5/6 下午8:30
# @Author  : daiyu
# @File    : 创建型模式-单例模式2.py
# @Software: PyCharm

# 这里使用方法 __new__来实现单例模式
# 实现__new__方法，并将一个类的实例绑定到类变量 _instance 上，
# 如果cls._instance为None说明该类还没有实例化过，实例化该类，并返回
# 如果cls._instance不为None，直接返回cls._instance

class Singleton(object): #抽象单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class MyClass(Singleton):
    a = 1

one = MyClass()
two = MyClass()

two.a = 3
print(one.a)
# 3

# one 和 two完全相同，可以用id(),==,is检测
print(id(one))
# 140719194494288
print(id(two))
# 140719194494288
print(one==two)
# True
print(one is two)
# True



