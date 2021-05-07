# 共享属性
# 所谓单例就是所有引用（实例、对象）拥有相同的状态（属性）和行为（方法）
# 同一个类的所有实例拥有相同的行为（方法）
# 只需要保证同一个类的所有实例具有相同的状态（属性）即可
# 所有实例共享属性的最简单最直接的方法就是__dict__属性指向（引用）同一个字典（dict）
# 可参考：http://code.activestate.com/recipes/66531/

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

    print(rm1.__dict__)
    print(rm2.__dict__)
    print(rm3.__dict__)
    print(rm4.__dict__)
    # {'state': 'Running'}



if __name__ == '__main__':
    main()
