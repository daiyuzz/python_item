"""
created by dyx on 2021/7/16.
"""

import multiprocessing


def func(my_dict, my_list):
    my_dict["index1"] = 'aaaa'
    my_dict["index2"] = "bbbb"
    my_list.append(11)
    my_list.append(22)
    my_list.append(33)


if __name__ == '__main__':
    with multiprocessing.Manager() as MG:
        my_dict = multiprocessing.Manager().dict()  # 主进程与子进程共享这个字典
        my_list = multiprocessing.Manager().list(range(5))  # 主进程

        p = multiprocessing.Process(target=func, args=(my_dict, my_list))
        p.start()
        p.join()

        print(my_dict)
        print(my_list)
