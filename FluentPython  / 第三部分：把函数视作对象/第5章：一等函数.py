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


"""
实现__call__方法的类是创建函数类对象的简便方式，此时必须在内部维护一个状态，让它在
调用之间可用
"""

"================================================================================"
# 5.6 函数内省
print(dir(factorial))

## dict

"""
与用户定义的常规类一样，函数适用 __dict__ 属性存储赋予它的用户属性。这相当于一种基于形式的注解。
一般来说，为函数随意赋予属性不是很常见的做法


在Django框架中，把 short_description 属性赋予一个方法，Django管理后台使用这个方法时，在记录
列表中会出现指定的描述文本：
"""


def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()


upper_case_name.short_description = 'Customer name'

"""
下面重点说明函数专有而用户定义的一般对象没有的属性
"""


class C: pass


obj = C()


def func(): pass


print(sorted(set(dir(func)) - set(dir(obj))))
# 常规对象没有而函数有的属性
# ['__annotations__', '__call__', '__closure__', '__code__', '__defaults__', '__get__', '__globals__', '__kwdefaults__', '__name__', '__qualname__']


"=================================================================================="

# 5.7 从定位参数到仅限关键字参数

"""
Python 最好的特性之一时提供了极为灵活的参数处理机制，而且Python3 进一步提供了仅限关键字参数。与之
密切相关的是，调用函数使用 * 和 ** 展开可迭代对象，映射到单个参数

"""


def tag(name, *content, cls=None, **attrs):
    """生成一个或多个HTML标签"""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join('%s="%s"' % (attr, value) for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)


print(tag('br'))  # 传入单个定位参数，生成一个指定名称的空标签
# <br/>

print(tag('p', 'hello'))  # 第一个参数后面的任意个参数会被 *content 捕获，存入一个元祖
# <p>hello</p>

print(tag('p', 'hello', 'world'))
# <p>hello</p>
# <p>world</p>

print(tag('p', 'hello', id=33))  # tag函数签名中没有明确指定名称的关键字参数会被 **attrs 捕获，存入一个字典
# <pid="33">hello</p>

print(tag('p', 'hello', 'world', cls='sidebar'))  # cls参数只能作为关键字参数传入
# <pclass="sidebar">hello</p>
# <pclass="sidebar">world</p>

print(tag(content='testing', name='img'))  # 调用tag函数时，即便第一个定位参数也能作为关键字参数传入
# <img content="testing" />


my_tag = {'name': 'img', 'title': 'Jack', 'src': 'sunset.jpg', 'cls': 'framed'}
print(tag(**my_tag))  # 在my_tag 前面加上 ** ，字段中的所有元素作为单个参数传入，同名键会绑定到对应的具名参数上，余下的则被 **attrs 捕获
# <img class="framed"src="sunset.jpg"title="Jack" />


"""
仅限关键字参数是 python3 新增的特性，上面cls参数只能通过关键字参数指定，它一定不会捕获未命名的定位参数。

定义函数时若想指定仅限关键字参数，要把它们放到前面有 * 的参数后面。如果不想支持数量不定的定位参数，
但想支持仅限关键字参数，在签名中放一个*，如下所示
"""


def f(a, *, b):
    return a, b


print(f(1, b=2))
# (1,2)

"""
注意：仅限关键字参数不一定要有默认值，可以像上面例子中b那样，强制必须传入实参。
"""

"======================================================================================="
# 5.8 获取关于参数的信息


import bobo


@bobo.query('/')
def hello(person):
    return 'Hello %s!' % person


"""
bobo.query 装饰器把一个普通的函数（如hello）与框架的请求处理机制结合起来。BoBo会内省hello函数，
发现它需要一个名为person的参数，然后从请求中获取那个名称对应的参数，将其传给hello参数，因此程序员根本
不用触碰请求对象


Bobo是怎么知道函数需要哪个参数呢？它又是怎么知道参数有没有默认值呢？


函数对象有一个 __defaults__ 属性，它的值是一个元祖，里面保存着定位参数和关键字参数的默认值。
仅限关键字参数的默认值在 __kwdefaults__ 属性中。然而，参数的名称在 __code__ 属性中，它的值是一个code
对象引用，自身也有很多属性。
"""


def clip(text, max_len=80):
    """在max_len前面或后面的第一个空格处截断文本"""
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:
        end = len(text)
    return text[:end].rstrip()


"======================================================================================="


# 5.9 函数注解

def clip(text: str, max_len: 'int>0' = 80) -> str:
    """在max_len前面或后面的第一个空格处截断文本"""
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:
        end = len(text)
    return text[:end].rstrip()


"""
有注解的函数声明

函数声明中的各参数可以在：之后增加注解表达式。如果参数有默认值，直接放在参数名和=号之间。
如果想注解返回值，在 ） 和函数声明末尾的 ： 之间添加 -> 和一个表达式。那个表达式可以使任何类型的

注解不会做任何处理，只是存储在函数的 __annotations__ 属性（一个字典）中



"""

print(clip.__annotations__)
# {'text': <class 'str'>, 'max_len': 'int>0', 'return': <class 'str'>}


"=================================================================================="
# 支持函数式编程的包

## operator模块


"""
在函数式编程中，经常需要把算术运算符当做函数使用
"""

from functools import reduce


def fact(n):
    return reduce(lambda a, b: a * b, range(1, n + 1))


"""
operator模块为多个算数运算符提供了对应的函数，从而避免编写lambda a,b:a*b 这种平凡的匿名函数
"""

from functools import reduce
from operator import mul


def fact(n):
    return reduce(mul, range(1, n + 1))
