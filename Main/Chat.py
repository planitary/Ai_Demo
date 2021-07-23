import logging,random
import pymysql
from Error_info import *
from Config import DbConfig
from Log import LogConfig
from Extra import AbstractChat,GetThirdinfo,GetToken

class ChatWithRobot(AbstractChat.Ai,BaseErrorInfo):
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

    def Chat(self):
        """用户登录后拿到token（暂未实现），Token目前写死"""
        db = self.__DbInit()
        cursor = db.cursor()
        specialId = -1
        username = 'jack'
        print('-----------Robot进入聊天室-----------\n输入quit可退出')
        logging.info("-----------聊天开始-----------")
        print('Robot:你好，我是robot，很高兴见到你')

        while 1:
            Token = GetToken.CreateToken(username).GetToken()
            Msg = input('jack:')
            """根据用户的话语，查询数据库找到AskForResponseId，与chat_response_data进行比对"""
            """判断用户所说的话是否为特殊话语（需要请求第三方应用）"""
            FindMsgSql = "select AskForResponseId,isSpecial,ClientAsk from chat_Resource_data where ClientAsk = '%s'" %Msg
            cursor.execute(FindMsgSql)
            result = cursor.fetchone()
            '''此处有bug，比对成功后还需判断是否已学习，此处没做判断，后面优化'''
            # 非特殊语句
            # 比对成功
            if result is not None and Msg != 'quit':
                specialId = result[1]
                AFRId = result[0]
                FindResponseByAFRId = "select Response from chat_response_data where ResponseToAskId = %d" % AFRId
                cursor.execute(FindResponseByAFRId)
                ResonseResult = cursor.fetchall()
                ResultSize = len(ResonseResult)
                if specialId != 1:
                    try:
                        if ResultSize is not 0:
                            # 找到所有匹配的组合后随机选取一个进行回答
                            logging.info('匹配成功')
                            ResponseSelect = random.randint(0,ResultSize - 1)
                            print('Robot:%s'% ResonseResult[ResponseSelect])
                        else:
                            raise MatchError(AFRId)
                    except Exception as e:
                        print(e)
                        logging.error('AskForResponseId:%d未匹配，请检查数据库'%AFRId)
            # 特殊语句
                else:
                    specialInfo = result[2]
                    # 检测到特殊语句中包含天气
                    if '天气' in specialInfo:
                        interFaceName = GetThirdinfo.GetWeather().getClassName()
                        logging.info('调用接口:%s'% interFaceName)
                        weatherInfo = GetThirdinfo.GetWeather().getWeather()
                        print("Robot:%s今天天气:%s,实时温度:%s,今天白天气温:%s,夜间气温:%s,空气指数:%s"%(
                        weatherInfo['city'],weatherInfo['weather'],weatherInfo['temperature'],
                        weatherInfo['tem_day'],weatherInfo['tem_night'],weatherInfo['air']))
                        logging.info('调用成功')
            # 比对失败
            elif result is  None and Msg != 'quit':
                '''没有在chat_resource_data中的数据表明没有学习过，先存入数据库，将isStudy字段设为0，后续更新'''
                print("Robot:这个问题我还没学会呢，等我学会了再来回答你吧~")
                logging.info("---------检测到新语句---------")
                sql = "insert into chat_resource_data(ClientToken,ClientAsk,isStudy) values ('%s','%s',0)" %(Token,Msg)
                cursor.execute(sql)
                db.commit()
                logging.info('---------新语句插入成功---------')
                # 特殊语句

            if Msg == 'quit':
                break
        print("Robot:欢迎下次再来~")
        logging.info("--------------聊天结束------------")

if __name__ == '__main__':
    newChat = ChatWithRobot()
    newChat.Chat()

