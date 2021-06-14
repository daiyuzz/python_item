# -*- coding: utf-8 -*-
# @Time    : 2021/5/9 下午9:38
# @Author  : daiyu
# @File    : 13.使用元类控制实例的创建.py
# @Software: PyCharm


class NoInstance(type):
    def __call__(self, *args, **kwargs):
        raise TypeError("Can`t instantite directly")


class Spam(metaclass=NoInstance):
    @staticmethod
    def grok(x):
        print("Spam.grok")


print(Spam.grok(42))


# Spam.grok

# s = Spam()


# TypeError: Can`t instantite directly


class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super(Singleton, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class Spam(metaclass=Singleton):
    def __init__(self):
        print('Creating Spam')


a = Spam()
# Creating Spam

b = Spam()
print(a is b)
# True
