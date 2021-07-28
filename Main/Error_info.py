class BaseErrorInfo(Exception):
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
class DbInitialError(BaseErrorInfo):
    def __init__(self,cursor):
        self.cursor = cursor
    def __str__(self):
        return '数据库链接失败'

class MatchError(BaseErrorInfo):
    def __init__(self,MatchId):
        self.Id = MatchId
    def __str__(self):
        return '匹配失败，错误码:%d' % self.Id

class ResultError(BaseErrorInfo):

    def __str__(self):
        return '条件未找到'

class IllegalUserError(BaseErrorInfo):
    def __init__(self):
        self.errCode = '000'

    def __str__(self):
        return "认证失败，非法操作!错误码:%s" % self.errCode


