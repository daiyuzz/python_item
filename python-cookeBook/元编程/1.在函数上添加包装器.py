import time
from functools import wraps


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result

    return wrapper


@timethis
def countdown(n):
    while n > 0:
        n -= 1


countdown(10000)
print(countdown.__name__)
print(countdown.__doc__)
print(countdown.__annotations__)

print(countdown.__wrapped__(10000))