# 7.1 装饰器的基本知识
"""
装饰器是可调用的对象，其参数是另一个函数（被装饰的函数）。装饰器可能会处理被装饰的函数，然后把它返回，或者将其替换成另一个函数或可调用对象
"""

"======================================================================================================================="

# 7.2 python 何时执行装饰器

"""
函数装饰器在导入模块时立即执行，而被装饰的函数只在明确调用时运行。这突出了python的导入时和运行时之间的区别



"""
"======================================================================================================================="

# 7.3 使用装饰器改进“策略模式”

promos = []  # promos 列表起初时空的


def promotion(promo_func):  # promotion 把 promo_func 添加到 promos列表中，然后原封不动的返回
    promos.append(promo_func)
    return promo_func


@promotion  # 被@promotion 装饰的函数都会添加到promos列表中
def fidelity(order):
    """为积分为1000或以上的顾客提供5%折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0


@promotion
def bulk_item(order):
    """单个商品为20或以上时提供10%折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount


@promotion
def large_order(order):
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0


def best_promo(order):  # best_promos 无需修饰，因为它依赖promos列表
    """选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)


"""
与6.1 节中给出的方案相比，这个方案有几个优点
- 促销策略函数无需使用特殊的名称（即不以_promo结尾）
- @promotion 在装饰器突出了被装饰的函数的作用，还便于临时禁用某个促销策略：只需要把装饰器注释掉即可
- 促销折扣策略可以在其他模块中定义，在系统任何的地方都行，只要使用 @promotion 装饰即可

"""

"======================================================================================================================="
# 7.4 变量作用域规则

# b = 6
#
#
# def f2(a):
#     print(a)
#     print(b)
#     b = 9
#
#
# print(f2(3))

"""
报错，b 打印失败
UnboundLocalError: local variable 'b' referenced before assignment

事实上，Python 编译函数的定义体时，它判断b是局部变量，以为在函数中给它赋值了。生成的字节码证实了这种判断，python会尝试从本地环境获取b。
后面调用f2(3) 时，f2的定义体会获取并打印局部变量a的值，但是尝试获取局部变量b的值时，发现b没有绑定值。

这不是缺陷，而是设计选择：Python不要求声明变量，但是假定在函数定义体中赋值的变量是局部变量。

如果在函数中赋值时想让解释器把b当成全局变量，要使用 global 声明：

b = 6
def f3(2):
    global b
    print(a)
    print(b)
    b = 9
    
f(3)
# 3
# 6

b
# 9

f(3)
# 3
# 9

b = 30
b
# 30


"""

"======================================================================================================================="

# 7.5 闭包

"""
闭包是一种函数，它会保留定义函数时存在的自由变量的绑定，这样调用函数时，虽然定义作用域不可用了，但是仍能使用那些绑定

注意：只有嵌套 在其他函数中的函数才可能需要处理不在全局作用域中的外部变量
"""

"======================================================================================================================="

# 7.6 nonlocal 声明

# def make_averager1():
#     count = 0
#     total = 0
#
#     def averager(new_value):
#         count += 1
#         total += new_value
#
#         return total / count
#
#     return averager


'----------------------------------------------------------'


def make_averager2():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return averager


"""
上述make_average1() 出现问题，当count 是数字或任何不可变类型时，count += 1语句的作用其实与count = count + 1一样。因此，我们在averager1的定义体中为count赋值了，
这会把count变成局部变量。total变量也受这个问题影响

make_average2() 没遇到这个问题，是因为我们没有给series赋值，我们只是调用了series.append 。并把它传给 sum 和 len 。也就是说，我们利用了列表时可变的对象
这一事实

但是对数字、元组、字符串等不可变类型来说，只能读取，不能更新。如果尝试重新绑定，例如count = count + 1。其实会隐式创建局部变量count。这样，count就不是
自由变量了，因此不会保存在闭包中

为了解决这个问题，python3中引入了 nonlocal 声明。它的作用是把变量标记为自由变量，即使在函数中为变量赋予新值，也会变成自由变量
如果为nonlocal声明的变量赋予新值，闭包中保存的绑定也会更新。
"""


def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count

    return averager


"======================================================================================================================="
# 7.7 实现一个简单的装饰器

## 下面示例定义了一个装饰器，他会在每次调用被装饰的函数时计时，然后把经过的时间、传入的参数和调用的结果打印出来

import time


def clock(func):
    def clocked(*args):  # 定义内部函数clocked，它接受任意个定位参数
        t0 = time.perf_counter()
        result = func(*args)  # 这行代码可用，是因为clocked的闭包中包含自由变量func
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ','.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result

    return clocked  # 返回内部函数，取代被装饰的函数。


@clock
def snooze(seconds):
    time.sleep(seconds)


@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


print('*' * 40, 'Calling snooze(.123)')
print(snooze(.123))

print('*' * 40, 'Calling factorial(6)')
print('6! = ', factorial(6))

"""
factorial 保存的是 clocked 函数的引用。自此之后，每次调用 factorial（n），执行的都是  clocked(n)。clocked大致做了下面几件事

1.记录初始时间 t0
2.调用原来的factorial函数，保存结果
3.计算经过的时间
4.格式化收集的数据，然后打印出来
4.返回第2步保存的结果



这是装饰器的典型行为：把被装饰的函数替换成新函数，二者接受相同的参数，而且（通常）返回被装饰的函数本该返回的值，同时还会做一些额外的操作
"""

import time
import functools


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(','.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(','.join(pairs))
        arg_str = ','.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result

    return clocked


print('*' * 40, 'Calling factorial(6)')
print('6! = ', factorial(6))

"======================================================================================================================="

# 7.8 标准库中的装饰器

"""
python 内置了三个用于装饰方法的函数：property、classmethod和staticmethod

另一个常见的装饰器是 functions.wraps 它的作用是协助构建行为良好的装饰器

标准库中最值得关注的两个装饰器是 lru_cache 和 singledispatch
"""

## 使用 functions.lru_cache做备份

"""
functions.lru_cache 是非常实用的装饰器，他实现了备忘的功能。这是一项优化技术，它把耗时的函数的结果保存起来，避免传入相同的参数时重复计算。
LRU 三个字母是“Least Recently Used”的缩写，表明缓存不会无限制增长，一段时间不用的缓存条目会被扔掉。



"""

import functools


@functools.lru_cache()  # 必须像常规函数那样调用lru_cache。这一行有一对括号，这么做的原因是 lru_cache 可以接受配置参数
@clock # 这里叠放了装饰器：@lru_cache() 应用到！@click 返回的函数上
def fibonaci(n):
    if n < 2:
        return n
    return fibonaci(n - 2) + fibonaci(n - 1)


print(fibonaci(6))

"""
除了优化递归算法之外，lru_cache 在从Web中获取信息的应用中也能发挥巨大作用

特别要注意，lru_cache 可以使用两个可选的参数来配置。它的签名是

functions.lru_cache(maxsize=128,typed=False)

maxsize 参数制定了存储多少个调用的结果。缓存满了之后，旧的结果会被扔掉，腾出空间。为了得到最佳性能，maxsize 应该设置为2的幂
typed参数如果设置为True，把不同参数类型得到的结果分开保存
"""

