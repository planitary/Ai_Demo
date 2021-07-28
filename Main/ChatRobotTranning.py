import random

import pymysql, logging,Login
from Config import DbConfig
from Log import LogConfig
from Extra import AbstractChat
from Error_info import IllegalUserError

class ChatRobot(AbstractChat.Ai, IllegalUserError):

    def __init__(self, UserToken):
        self.token = UserToken

    # 鉴权机制
    def __Authorize(self):
        ErrorCode = 0
        try:
            if self.token == '':
                ErrorCode = -1
                raise IllegalUserError
        except Exception as e:
            print(e)
            logging.error("非法操作，无法获取用户身份!")
        return ErrorCode
    '''用户语句与机器人响应为多对多，用户的AskForResponseId 与响应码RosponseToAskId一致时，为一组合适的匹配'''
    """对机器人的回答做出限制，凡是带有问号的全部为疑问句，方便机器人模拟回答，（暂未实现）"""
    AskForResponseId = 0
    RosponseToAskId = 0

    def __DbInit(self):
        db_dict = {'name': DbConfig.user,
                   'pwd': DbConfig.password,
                   'port': DbConfig.port,
                   'db': DbConfig.db,
                   'charset': DbConfig.charset,
                   'host': DbConfig.host}
        # 数据库锚点,用于向异常类传递数据库连接
        cursor = 1
        # 链接数据库
        if self.token != -1:
            conn = pymysql.connect(host=db_dict['host'], user=db_dict['name'], password=db_dict['pwd'],
                               db=db_dict['db'], charset=db_dict['charset'])
            return conn

    # 聊天训练模块
    def ChatTranning(self):
        # 鉴权，检测不到用户直接退出
        if self.__Authorize() == -1:
            return False
        else:
            cur = self.__DbInit()
            AskCount = 0                               # 统计训练数量
            ReponseCount = 0
            cursor = cur.cursor()
            flag = 1
            endOtherResponse = 1                     # 判断是否还有别的响应
            endOtherAsk = 1                          # 判断是否还有别的语句
            isSpecial = -1                  # 判断是否为特殊语句
            findUsernameByTokenSql = "select name from users where token = '%s'" %self.token
            cursor.execute(findUsernameByTokenSql)
            UserResult = cursor.fetchone()
            UserName = UserResult[0]

        """扫描数据库，看是否有数据，有数据时拿到最后一条记录的askid，用于继续向数据库添加学习数据
        如果没有的话就从第一次开始"""
        findAskId = "select AskForResponseId from chat_resource_data where AskForResponseId > -1 " \
                    "order by id desc limit 1"
        cursor.execute(findAskId)
        AskResult = cursor.fetchone()
        if AskResult is not None:
            self.AskForResponseId = AskResult[0] + 1
            self.RosponseToAskId = AskResult[0] + 1

        while flag:
            print('--------------训练开始------------')
            logging.info("----------------训练开始--------------")
            logging.info('----------------用户发起聊天----------------')
            while endOtherAsk:
                print("Robot: 你会说什么呢?")
                ClientMsg = input()
                findIsStudySql = "select * from Chat_Resource_Data where ClientAsk = '%s'" % ClientMsg
                cursor.execute(findIsStudySql)
                result = cursor.fetchone()
                if result is not None:
                    print('该语句已存在')
                else:
                    # 检测是否特殊语句
                    str1 = '天气'
                    str2 = '？'
                    if str1 in ClientMsg and str2 in ClientMsg:
                        logging.info('特殊语句')
                        SpecialResponseSql = "insert into Chat_Resource_Data " \
                                         "(ClientToken,ClientAsk,AskForResponseId,isStudy,isSpecial) " \
                                         "values('%s','%s',-1,1,1)" % (UserName, ClientMsg)
                        cursor.execute(SpecialResponseSql)
                        cur.commit()
                        logging.info('特殊语句插入成功')
                        isSpecial = 1
                    else:
                        TrainningInsertSql = "insert into Chat_Resource_Data " \
                                         "(ClientToken,ClientAsk,AskForResponseId,isStudy) " \
                                         "values('%s','%s',%d,1)" % (UserName, ClientMsg, self.AskForResponseId)
                        cursor.execute(TrainningInsertSql)
                        cur.commit()
                    endOtherAsk = int(input('你还有其他的么? 1:有 0:没有\n'))
                    AskCount += 1
            self.AskForResponseId += 1
            if endOtherAsk == 0:
                logging.info("用户语句插入成功，对应应答族id:%d" % self.AskForResponseId)

            logging.info('----------------机器人响应回答----------------')
            while endOtherResponse:
                if isSpecial == 1:
                    print("Robot:特殊语句")
                    ReponseCount += 1
                    endOtherResponse = 0
                else:
                    print("Robot:你希望我怎样回答?")
                    RobotMsg = input()
                    TrainningInsertSql = "insert into chat_response_data(ResponseToAskId,Response) values " \
                                        "(%d,'%s')" % (self.RosponseToAskId, RobotMsg)
                    cursor.execute(TrainningInsertSql)
                    cur.commit()
                    endOtherResponse = int(input('还有别的回答么?  1:有 0:没有\n'))
                    ReponseCount += 1
            self.RosponseToAskId += 1
            if endOtherResponse == 0:
                logging.info("机器人响应语句插入成功，响应id族:%d" % self.RosponseToAskId)
            flag = int(input('是否结束训练？   0：是   1：不是'))
            # 重置参数，开始下一轮训练
            endOtherAsk = 1
            endOtherResponse = 1
            isSpecial = -1
        print('--------------训练结束------------')
        logging.info('----------------训练结束,共训练成功语句%d条，响应%d条----------------' % (AskCount,ReponseCount))




if __name__ == '__main__':
    newTrainning = ChatRobot('')
    newTrainning.ChatTranning()
