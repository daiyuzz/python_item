class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class YourBorg(Borg):
    def __init__(self, state=None):
        super(YourBorg, self).__init__()
        if state:
            self.state = state
        else:
            if not hasattr(self, "state"):
                self.state = "Init"

    def __str__(self):
        return self.state


def main():
    rm1 = YourBorg()
    rm2 = YourBorg()

    rm1.state = "Idle"
    rm2.state = "Running"

    print('rm1: {0}'.format(rm1))
    # rm1: Running

    print('rm2: {0}'.format(rm2))
    # rm2: Running

    rm2.state = 'Zombie'
    print('rm1: {0}'.format(rm1))
    # rm1: Zombie
    print('rm2: {0}'.format(rm2))
    # rm2: Zombie

    # 尽管rm1和rm2共性属性，但是rm1和rm2并不相同
    print(rm1 is rm2)
    # False

    # 新的实例也会共享状态
    rm3 = YourBorg()
    print('rm1: {0}'.format(rm1))
    # rm1: Zombie
    print('rm2: {0}'.format(rm2))
    # rm2: Zombie
    print('rm3: {0}'.format(rm3))
    # rm3: Zombie

    # 新实例可以在创建的时候显示的改变状态
    rm4 = YourBorg("Running")
    print('rm4: {0}'.format(rm4))
    # rm4: Running
    print('rm2: {0}'.format(rm2))
    # rm2: Running


if __name__ == '__main__':
    main()
