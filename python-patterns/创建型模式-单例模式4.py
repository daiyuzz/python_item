# -*- coding: utf-8 -*-
# @Time    : 2021/5/7 上午8:52
# @Author  : daiyu
# @File    : 创建型模式-单例模式4.py
# @Software: PyCharm


# 方法4：也是方法2的升级版，
# 使用装饰器（decorator）
# 这是一种更pythonic，更elegant的方法
# 单例本身不知道自己是单例，因为它本身（自己的代码）并不是单例


def singleton(cls,*args,**kwargs):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return _singleton

@singleton
class MyClass(object):
    a = 1

    def __init__(self,x=0):
        self.x = x

one = MyClass()
two = MyClass()

two.a =3
print(one.a)
# 3

print(id(one))
# 140381565963328
print(id(two))
# 140381565963328

print(one==two)
# True

print(one is two)
# True

one.x = 2
