"""
created by dyx on 2021/7/16.
"""

import multiprocessing


def func(num):
    num[2] = 999  # 子进程改变数组，主进程跟着改变


if __name__ == '__main__':
    num = multiprocessing.Array("i", [1, 2, 3, 4, 5])  # 主进程和子进程共享这个数组
    print(num[:])

    p = multiprocessing.Process(target=func, args=(num,))
    p.start()
    p.join()

    print(num[:])
