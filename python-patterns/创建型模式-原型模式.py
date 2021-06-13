# -*- coding: utf-8 -*-
# @Time    : 2021/6/13 上午10:59
# @Author  : daiyu
# @File    : 创建型模式-原型模式.py
# @Software: PyCharm


# 图层对象
from copy import copy, deepcopy


class simpleLayer:
    background = [0, 0, 0, 0]
    content = 'blank'

    def getContent(self):
        return self.content

    def getBackground(self):
        return self.background

    def paint(self, painting):
        self.content = painting

    def setParent(self, p):
        self.background[3] = p

    def fillBackground(self, back):
        self.background = back

    def clone(self):
        return copy(self)

    def deep_clone(self):
        return deepcopy(self)


# 新建图层，填充蓝底并画一只狗，可以简单表示如下：

if __name__ == '__main__':
    dog_layer = simpleLayer()
    dog_layer.paint("Dog")
    dog_layer.fillBackground([0, 0, 255, 0])
    print("Background:", dog_layer.getBackground())
    print("Painting:", dog_layer.getContent())
    another_dog_layer = dog_layer.clone()
    print("Background:", another_dog_layer.getBackground())
    print("Painting:", another_dog_layer.getContent())
