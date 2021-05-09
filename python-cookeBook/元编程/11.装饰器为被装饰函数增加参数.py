# -*- coding: utf-8 -*-
# @Time    : 2021/5/9 下午8:12
# @Author  : daiyu
# @File    : 11.装饰器为被装饰函数增加参数.py
# @Software: PyCharm

from functools import wraps


def option_debug(func):
    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)

    return wrapper


@option_debug
def spam(a, b, c):
    print(a, b, c)


print(spam(1, 2, 3))
# 1 2 3

print(spam(1, 2, 3, debug=True))
# Calling spam
# 1 2 3


from functools import wraps
import inspect


def option_debug(func):
    if 'debug' in inspect.getargspec(func).args:
        raise TypeError('Debug argument already defined')

    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print("Calling", func.__name__)
        return func(*args, **kwargs)

    return wrapper


@option_debug
def a(x):
    pass


@option_debug
def b(x, y, z):
    pass


@option_debug
def c(x, y):
    pass
