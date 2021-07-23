import pymysql, logging
from Config import DbConfig
from Log import LogConfig
from Extra import GetToken,AbstractChat
from Error_info import *


class ChatRobot(BaseErrorInfo,AbstractChat.Ai):

    # 全局计数，用于向Chat_Resource_Data库中添加用户话语id
    AskForResponseId = 0
    # 全局计数，用于向Chat_Response_Data库中添加机器人响应话语id
    '''用户语句与机器人响应为多对多，用户的AskForResponseId 与响应码RosponseToAskId一致时，为一组合适的匹配'''
    """对机器人的回答做出限制，凡是带有问号的全部为疑问句，方便机器人模拟回答，（暂未实现）"""
    RosponseToAskId = 0
    @classmethod
    def __DbInit(cls):
        db_dict = {'name': DbConfig.user,
                   'pwd': DbConfig.password,
                   'port': DbConfig.port,
                   'db': DbConfig.db,
                   'charset': DbConfig.charset,
                   'host': DbConfig.host}
        # 数据库锚点,用于向异常类传递数据库连接
        cursor = 1
        # 链接数据库
        conn = pymysql.connect(host=db_dict['host'], user=db_dict['name'], password=db_dict['pwd'],
                               db=db_dict['db'], charset=db_dict['charset'])
        return conn

    # 聊天训练模块
    def ChatTranning(self):
        """获取训练者token，从登录接口获取，暂未实现，写死为jack"""
        cur = self.__DbInit()
        AskCount = 0                               # 统计训练数量
        ReponseCount = 0
        cursor = cur.cursor()
        flag = 1
        endOtherResponse = 1                     # 判断是否还有别的响应
        endOtherAsk = 1                          # 判断是否还有别的语句
        isSpecial = -1                  # 判断是否为特殊语句
        while flag:
            print('--------------训练开始------------')
            logging.info("----------------训练开始--------------")
            logging.info('----------------用户发起聊天----------------')
            while endOtherAsk:
                Token = GetToken.CreateToken('jack').GetToken()
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
                                         "values('%s','%s',-1,1,1)" % (Token, ClientMsg)
                        cursor.execute(SpecialResponseSql)
                        cur.commit()
                        logging.info('特殊语句插入成功')
                        isSpecial = 1
                    else:
                        TrainningInsertSql = "insert into Chat_Resource_Data " \
                                         "(ClientToken,ClientAsk,AskForResponseId,isStudy) " \
                                         "values('%s','%s',%d,1)" % (Token, ClientMsg, self.AskForResponseId)
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
    newTrainning = ChatRobot()
    newTrainning.ChatTranning()
