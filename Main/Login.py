import pymysql,hashlib
from Config import DbConfig
import time
import logging
from Log import LogConfig
from Extra import GetToken
class Login:
    # 用户token
    UserToken = ''
    '''链接数据库'''
    # 数据库初始化配置
    @classmethod
    def _init_Db(self, data=None):
        db_dict = {'name':DbConfig.user,
               'pwd':DbConfig.password,
               'port':DbConfig.port,
               'db':DbConfig.db,
               'charset':DbConfig.charset,
               'host':DbConfig.host}
        # 数据库锚点,用于向异常类传递数据库连接
        cursor = 1
        # 链接数据库
        conn = pymysql.connect(host=db_dict['host'],user=db_dict['name'],password=db_dict['pwd'],
                               db=db_dict['db'],charset=db_dict['charset'])
        return conn

    # def CreateTable(self):
    # 注册
    def Register(self):
        # 链接数据库
        conn = self._init_Db()
        flag = -1                       # 注册完成的标志
        # 生成游标对象
        cur = conn.cursor()
        while flag == -1:
            print("##################################################\n                       注册页面\n"
                  "##################################################")
            _user = input('请输入用户名:')
            pwd = input('请输入密码:')
            Reg_find_sql = "select * from student where name = '%s'" % _user
            cur.execute(Reg_find_sql)
            result = cur.fetchall()
            '''fetchall,fetchone等方法返回的是一个元组'''
            # 如果没有数据，则插入新用户数据，密码为md5加密
            if len(result) == 0:
                logging.info('注册成功，用户名:%s' % _user)
                insert_sql = "insert into student(name,password) values ('%s',md5('%s'))" % (_user, pwd)
                cur.execute(insert_sql)
                conn.commit()  # 增删改需要先commit
                logging.info("数据插入成功，insert into student('???','???') values (???,???)")
                Token_ = GetToken.CreateToken().GeneratorSerialize(_user)
                '''插入用户对应token'''
                insert_token_sql = "update student set token = '%s' where name = '%s'"%(Token_,_user)
                cur.execute(insert_token_sql)
                conn.commit()
                flag = 0
                return flag
            else:
                print('用户名存在，请重新输入')
    # 登录
    def Login_(self):
        conn = self._init_Db()
        isNeedReg = 0              # 是否需要注册
        cursor = conn.cursor()
        isLog = len(self.UserToken)         #登录完成的标志
        while isLog == 0:
            _user = input('请输入用户名:')
            pwd = input('请输入密码:')
            login_find_sql = "select name,password,token from student where name = '%s'" % (_user)
            cursor.execute(login_find_sql)
            find_result = cursor.fetchone()
            # 用户输入的密码加密后与数据库比对
            hashPwd = hashlib.md5()
            hashPwd.update(pwd.encode('utf8'))
            hashPwd_ = hashPwd.hexdigest()
            # 如果找到了对应数据
            if find_result != None:
                if hashPwd_ == find_result[1] and _user == find_result[0]:
                    logging.info('%s登录成功' %_user)
                    self.UserToken = find_result[2]
                    print("登录成功")
                    print("欢迎%s" % _user)
                    return isNeedReg
                elif hashPwd_ != find_result[1] and _user == find_result[0]:
                    print('密码错误，请重新输入')
            else:
                isNeedReg = 1
                print("没有账户，请注册!")
                return isNeedReg

    def getToken(self):
        return self.UserToken


if __name__ == '__main__':
    Start = Login()
    # df = Start.Login_()
    count = 0
    tokenLength = 0
    '''一开始没有信息，无token，需要登录'''
    while count <= 5:
        if tokenLength != 0:
            count += 1
            print('请计算')
        else:
            time.sleep(1.4)
            print("检测到您还没有登录，请先登录!")
            '''获取登录信息，如果登录成功，刷新token(函数内部刷新)与flag值，表示不用注册，执行后续内容'''
            RegFlag = Start.Login_()
            if RegFlag == 0:
                # token计数，如果成功获取到一次token，则下次循环不在重复获取
                # 登录成功后会拿到token
                token = Start.getToken()
                tokenLength = len(token)
            elif RegFlag == 1:
                EndReg = Start.Register()
                if EndReg == 0:
                    print('注册成功')
                    time.sleep(1.3)






