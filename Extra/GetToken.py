import time
import hashlib

class CreateToken():
    # 生成时间戳
    global t_stamp

    @classmethod
    def __init__(self,user):
        self.username = user
        t = time.time()
        self.t_stamp = int(t)


    # 生成token
    @classmethod
    def __GeneratorSerialize(self,user):
        _token = str(self.t_stamp) + str(user)
        # 用sha算法对token加密，指定utf8的编码
        Serialize = hashlib.sha1()
        Serialize.update(_token.encode("utf8"))
        return Serialize.hexdigest()

    # 获取token
    def GetToken(self):
        self.__Token = self.__GeneratorSerialize(self.username)
        return self.__Token

        # print(token)
