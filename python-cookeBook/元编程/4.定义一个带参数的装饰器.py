# 假设你想写一个装饰器，给函数添加日志功能，同时允许用户指定日志的级别和其他的选项


from functools import wraps
import logging


def logged(level, name=None, message=None):
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        return wrapper

    return decorate


@logged(logging.DEBUG)
def add(x, y):
    return x + y


print(add(3, 4))


@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam')
