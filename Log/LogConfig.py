import logging
import time


# 格式化日志，指定格式
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# 格式化日期
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
str = time.strftime("%Y%m%d-%H-%M-%S",time.localtime())
# windows日志路径
# logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT,filename='Log\%s.log' % str)
# mac日志路径
logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT,filename='../Log/%s.log' % str)
