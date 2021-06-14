# -*- coding: utf-8 -*-
# @Time    : 2021/6/13 下午1:10
# @Author  : daiyu
# @File    : 结构型模式-代理模式.py
# @Software: PyCharm


# 首先，构造一个网络服务器
info_struct = dict()
info_struct["addr"] = 10000
info_struct["content"] = ""


class Server:
    content = ""

    def recv(self, info):
        pass

    def send(self, info):
        pass

    def show(self):
        pass


class infoServer(Server):
    def recv(self, info):
        self.content = info
        return "recv OK !"

    def send(self, info):
        pass

    def show(self):
        print("SHOW:%s" % self.content)


# 如何给这个服务器设置一个白名单，使得只有白名单里的地址可以访问服务器呢？
# 修改Server结构是个方法，但这显然不符合软件设计原则中的单一职责原则。在此基础之上，使用代理，是个不错的方法。代理配置如下：

class serverProxy:
    pass


class infoServerProxy(serverProxy):
    server = ""

    def __init__(self, server):
        self.server = server

    def recv(self, info):
        return self.server.recv(info)

    def show(self):
        self.server.show()


class whiteInfoServerProxy(infoServerProxy):
    white_list = []

    def recv(self, info):
        try:
            assert type(info) == dict
        except:
            return "info structure is not correct"
        addr = info.get("addr", 0)
        if not addr in self.white_list:
            return "Your address is not in the whit list"
        else:
            content = info.get("content", "")
            return self.server.recv(content)

    def addWhite(self, addr):
        self.white_list.append(addr)

    def rmvWhite(self, addr):
        self.white_list.remove(addr)

    def clearWhite(self):
        self.white_list = []


if __name__ == '__main__':
    info_struct = dict()
    info_struct["addr"] = 10010
    info_struct["content"] = "Hello World!"
    info_server = infoServer()
    info_server_proxy = whiteInfoServerProxy(info_server)
    print(info_server_proxy.recv(info_struct))
    info_server_proxy.show()
    info_server_proxy.addWhite(10010)
    print(info_server_proxy.recv(info_struct))
    info_server_proxy.show()
