# -*- coding: utf-8 -*-
# @Time    : 2021/5/8 上午8:20
# @Author  : daiyu
# @File    : 8.将装饰器定义为类的一部分.py
# @Software: PyCharm

from functools import wraps


class A:

    def decorator1(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("Decorator 1")
            return func(*args, **kwargs)

        return wrapper

    @classmethod
    def decorator2(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("Decorator 2")
            return func(*args, **kwargs)

        return wrapper


a = A()


@a.decorator1
def spam():
    pass


@A.decorator2
def grok():
    pass
