# -*- coding: utf-8 -*-
# @Author  : daiyu
# @File    : 第2章：序列构成和数组.py
# @Description : 数据结构
# @Time    : 2020/11/27 下午1:14


# 内置序列类型
"""
容器序列
    list、tuple和collections.deque 这些序列能存放不同类型的数据

扁平序列
    str、bytes、bytearray、memoryview和array.array 这类序列只能容纳一种类型。

容器序列存放的是它们包含的任意类型的对象的引用，而扁平序列里面存放的是值而不是引用
换句话说，扁平序列其实是一段连续的内存空间



序列类型还可以按照能够被修改来分类

可变序列：
    list、bytearray、array.array、collections.deque 和 memoryview

不可变序列：
    tuple、str 和 bytes
"""

# 列表推到和生成器表达式

"""
列表推导不会再有变量泄露的问题

filter和map合起来能做的事，列表推导也可以，而且还不需要借助难以理解和阅读的 lambda表达式
"""

# 生成器表达式

"""
虽然也可以用列表推导式来初始化元祖、数组或其他序列类型，但是生成器表达式是更好的选择。这是因为生成器表达式背后遵守了迭代器协议，可以逐个
产出元素，而不是先建立一个完整的列表，然后再把这个列表传递到某个构造函数里，显然能够更节省内存。

生成器表达式的语法跟列表推导式差不多，只不过把方括号换成圆括号而已
"""

# 元组不仅仅是不可变的列表

"""

把元组用作记录


元组拆包

元祖拆包可以应用到任何可迭代对象上，唯一的硬性要求是，被可迭代对象中的元素数量必须要跟接受这些元素的元组的空挡数一致，
除非我们用 * 来表示忽略多余的元素


在元组拆包中使用*也可以帮助我们把注意力集中在元组的部分元素上

用*来处理剩下的元素

"""

## 嵌套元组拆包

"""
接受表达式的元组可以使嵌套的，例如（a,b,(c,d)）。只要这个接受元组的嵌套结构符合表达式本身的嵌套结构，python就会做出正确的应对
"""

## 具名元组

"""
collections.namedtuple 是一个工厂函数，它可以用来构建一个带字段名元组和一个有名字的类--这个带名字的类对调试程序有很大帮助
"""

"""
用 namedtuple 构建的类的实例所消耗的内存跟元组是一样的，因为字段名都被存在对应的类里面。这个实例跟普通的对象实例比起来要小一些，
因为python不会用 __dict__ 来存放这些实例的属性

"""

from collections import namedtuple

City = namedtuple('City', 'name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
# tokyo
City(name='Tokyo', country='JP', population=36.933, coordinates=(35.689722, 139.691667))
tokyo.population
# 36.933
tokyo.coordinates
# (35.689722, 139.691667)
tokyo[1]
# 'JP'

"====================================================================================================="

# 切片

