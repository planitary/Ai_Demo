import time
import hashlib

class CreateToken():
    # 生成时间戳
    global t_stamp
    @classmethod
    def __init__(self):
        t = time.time()
        self.t_stamp = int(t)

    # 生成token
    @classmethod
    def GeneratorSerialize(self,user):
        self.user = user
        _token = str(self.t_stamp) + str(self.user)
        # 用sha算法对token加密，指定utf8的编码
        Serialize = hashlib.sha1()
        Serialize.update(_token.encode("utf8"))
        token = Serialize.hexdigest()
        return token
        # print(token)

