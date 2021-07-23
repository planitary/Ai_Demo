import logging
import time


# 格式化日志，指定格式
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# 格式化日期
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
str = time.strftime("%Y%m%d-%H-%M-%S",time.localtime())

'''不同系统下的日志路径，非绝对，需根据实际情况进行变更'''
# windows日志路径
'''格式化输出日志，其中filemode指定日志文件写入方式，'a'为追加，'w'为覆盖，默认为追加'''
# logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT,
#                     filename='..\Log\%s.log' % str)
# windows日志配置
# logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT,
#                     filename='../Log/%s.log' % str,filemode='a',encoding = 'utf-8')

# mac日志配置
logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT,
                    filename='../Log/%s.log' % str,filemode='a')
