from abc import ABCMeta,abstractmethod

# AI组抽象类，抽象方法实现在具体的类中
class Ai(metaclass=ABCMeta):
    # 机器聊天抽象方法
    @abstractmethod
    def Chat(self):
        pass
    # 机器学习抽象方法
    @abstractmethod
    def ChatTranning(self):
        pass