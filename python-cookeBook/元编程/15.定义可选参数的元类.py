from abc import ABCMeta, abstractmethod


class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxsize=None):
        pass

    @abstractmethod
    def write(self, data):
        pass


class MyMeta(type):
    # Optional
    @classmethod
    def __prepare__(metacls, name, bases, *, debug=False, synchronize=False):
        pass
        return super(MyMeta, metacls).__prepare__(name, bases)

    # Required
    def __new__(cls, name, bases, ns, *, debug=False, synchronize=False):
        # Custom processing
        pass
        return super(MyMeta, cls).__new__(cls, name, bases, ns)

    # Required
    def __init__(self, name, bases, ns, *, debug=False, synchronize=False):
        # Custom processing
        pass
        super(MyMeta, self).__init__(name, bases, ns)
