class BaseErrorInfo(Exception):
    "自定义异常，检测类型错误时抛出类型不符合"
    "所有异常类的基类"
    pass

class BuildError(BaseErrorInfo):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return '此条件下无法构成'+self.msg + '!'

class PositiveIntegerError(BaseErrorInfo):
    def __init__(self):
        pass

    def __str__(self):
        return '请输入大于0的数'


