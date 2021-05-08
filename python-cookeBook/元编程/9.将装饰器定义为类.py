# -*- coding: utf-8 -*-
# @Time    : 2021/5/8 上午8:40
# @Author  : daiyu
# @File    : 9.将装饰器定义为类.py
# @Software: PyCharm

import types
from functools import wraps


class Profiled:

    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)  # 将方法动态的绑定到实例上


@Profiled
def add(x, y):
    return x + y


class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)


print(add(2, 3))
# 5

print(add(4, 5))
# 9

print(add.ncalls)
# 2

s = Spam()
print(s.bar(1))
# <__main__.Spam object at 0x7f3b9ffdbcd0> 1

print(s.bar(2))
# <__main__.Spam object at 0x7f3b9ffdbcd0> 2

print(s.bar(3))

# <__main__.Spam object at 0x7f3b9ffdbcd0> 3

print(Spam.bar.ncalls)
# 3


s = Spam()
def  grok(self,x):
    pass

print(grok.__get__(s,Spam))
# <bound method grok of <__main__.Spam object at 0x7fc765c26ca0>>

