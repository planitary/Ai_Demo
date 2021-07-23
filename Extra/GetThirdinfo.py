import json,requests

from Extra import GetIp


class GetWeather():
    # 获取天气接口的静态变量
    @classmethod
    def __init__(cls):
        cls.__appid = '81849973'
        cls.__secretkey = 'Ek6oo9W8'
        cls.__ip = GetIp.getIp()

    def getWeather(self):
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

d = GetWeather()
print(d.getClassName())