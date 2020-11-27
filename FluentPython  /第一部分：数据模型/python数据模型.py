# -*- coding: utf-8 -*-
# @Author  : daiyu
# @File    : python数据模型.py`
# @Description : python 数据模型
# @Time    : 2020/11/26 下午8:43

import collections

# namedtuple 用来构建只有少数属性但是没有方法的对象
Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds cluds hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]


beer_card = Card('7', 'diamonds')
print(beer_card)

deck = FrenchDeck()
print(len(deck))

# deck[0] 由 __getitem__方法提供
print(deck[0])
print(deck[-1])

from random import choice

print(choice(deck))

"""
 - 作为你的类的用户，他们不必去记住标准操作的各式名称（怎么得到元素的总和？是.size()还是.length()还是别的什么？）
 - 可以更加方便的利用python标准库，比如 random.choice函数，从而不用重新发明轮子




因为 __getitem__方法把[] 操作交给了self._cards 列表，所以我们的deck 类自动支持切片操作
"""

print(deck[:3])

# [Card(rank='2', suit='spades'), Card(rank='3', suit='spades'), Card(rank='4', suit='spades')]

# 先抽出所以为12的那张牌，然后每隔13张牌拿一张
print(deck[12::13])
# [Card(rank='A', suit='spades'), Card(rank='A', suit='diamnds'), Card(rank='A', suit='cluds'), Card(rank='A', suit='hearts')]

"""
另外，仅仅实现了 __getitem__ 方法，这一摞牌就变成可迭代的了
"""
for card in deck:
    print(card)

# 反向迭代也没关系
for card in reversed(deck):
    print(card)

"""
迭代通常是隐式的，比如说一个集合类型没有实现 __contains__ 方法，那么 in 运算符就会按顺序做一次迭代搜索。
于是，in 运算符可以用我们的 FrenchDeck 类上，因为它是可迭代的
"""

print(Card('Q', 'hearts') in deck)
# True

print(Card('7', 'beasts') in deck)
# False

"""
那么排序呢？我们按照常规，用点数来判定扑克牌的大小，2最小，A最大；同时还加上对花色的判定，黑桃最大、红桃次之，方块再次之，梅花最小
下面就是按照这个规则来给扑克牌排序的函数，梅花2的大小为0，黑桃A是51
"""

suit_values = dict(spades=3, hearts=2, diamonds=1, cluds=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


# 有了 spades_high函数，就能对这摞牌进行升序排序了
for card in sorted(deck, key=spades_high):
    print(card)

"""
虽然 FrenchDeck 隐式地继承了 Object 类，但功能确实不是继承而来的。我们通过数据模型和一些合成来实现这些功能。通过实现 __len__和 __getitem__
这两个特殊方法， FrenchDeck 就跟一个 Python 自有的序列数据类型一样。
"""

## 如何洗牌
"""
设置 __setitem__方法
"""

"=========================================================================================================="

# 模拟数值类型

""""
实现一个Vector类，包含特殊方法： __repr__, __abs__, __add__和 __mul__

"""

from math import hypot


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector(%r,%r)' % (self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)


# 虽然代码里有6个特殊方法，但这些方法（除了__init__）并不会在这个类自身代码中使用。


print(Vector(6, 8) + Vector(3, 2))

"======================================================================================================"

# 字符串表示形式

"""
python 有一个内置的函数叫 repr ，它能把一个对象用字符串的形式表达出来以辨认，这就是“字符串表达形式”，如果没有实现__repr__，当我们在控制台里打印一个向量实例时，
得到的字符串可能会是<Vector object at 0x10e100070>。
"""

"======================================================================================================"

# 算术运算符

"""
通过 __add__ 和 __mul__，示例 1-2 为向量类带来了 + 和 * 这两个算
术运算符。值得注意的是，这两个方法的返回值都是新创建的向量对
象，被操作的两个向量（self 或 other）还是原封不动，代码里只是
读取了它们的值而已

中缀运算符的基本原则就是不改变操作对象，而是产出一个新的值


"""

"======================================================================================================="
# 自定义的布尔值


"""
默认情况下，我们自定定义的类的实例总是被认为是真的，除非这个类对 __bool__ 或者 __len__ 函数有自己的实现。 
bool(x) 的背后是调用 x.__bool__()的结果；如果不存在 __bool__ 方法，那么bool(x) 会尝试调用 x.__len__().若返回
0，则bool会返回False；否则返回True


我们对 __bool__ 的实现很简单，如果一个向量的模是 0，那么就返回
False，其他情况则返回 True。因为 __bool__ 函数的返回类型应该
是布尔型，所以我们通过 bool(abs(self)) 把模值变成了布尔值。


"""

# 特殊方法总览



