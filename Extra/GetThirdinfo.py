import json,requests,re
import logging

from Main.Error_info import ResultError


class GetIp(ResultError):

    def Ip(self):
        try:
            text = requests.get("http://baidu.com").text
            ip = re.findall(r'\d+.\d+.\d+.\d+', text)
            if len(ip) is 0:
                raise ResultError
        except Exception as e:
            print(e)
            logging.error("查询失败，未找到正确的ip")
        else:
            return ip[0]

    def getIp(self):
        self.ip = self.Ip()
        return self.ip

    def getClassName(self):
        name = self.__class__.__name__
        return name

class GetWeather:
    # 获取天气接口的静态变量
    @classmethod
    def __init__(cls):
        cls.__appid = '81849973'
        cls.__secretkey = 'Ek6oo9W8'

    def getWeather(self):
        """接口保护机制：该接口默认什么都不传，会根据当前的调用ip返回天气，getIp方法不通过也不影响该接口的调用"""
        interfaceName = GetIp().getClassName()
        logging.info('调用接口:%s'% interfaceName)
        self.__ip = GetIp().Ip()
        method = 'GET'
        url = 'https://tianqiapi.com/free/day'
        params = {
            'appid':self.__appid,
            'appsecret':self.__secretkey,
            'ip':self.__ip
        }
        response_ = requests.request(method= method,url=url,params = params)
        response = response_.text
        response = json.loads(response)
        # print(response)
        # 天气数据
        weatherData = {
            'city':response['city'],
            'weather':response['wea'],
            'temperature':response['tem'],
            'tem_day':response['tem_day'],
            'tem_night':response['tem_night'],
            'air':response['air']
        }
        return weatherData

    # 获取类名，供打印日志使用
    def getClassName(self):
        name = self.__class__.__name__
        return name

