import math,logging
from Error_info import *
from Log import LogConfig

class Cal_Voume(BaseErrorInfo):
    @classmethod
    def __init__(self):
        logging.info("Start")

    # 长方体
    def Cuboid(self,length,width,height):
        try:
            if length < 0 or height < 0 or width < 0 :
                raise PositiveIntegerError
        except Exception as e:
            print(e)
            if length < 0 :
                logging.error("-----****长%d不合法***-----" % length, exc_info=True, stack_info=True)
            if height < 0:
                logging.error("-----****高%d不合法***-----" % height, exc_info=True, stack_info=True)
            if width < 0:
                logging.error("-----****宽%d不合法***-----" % width, exc_info=True, stack_info=True)
        else:
            Volume = length * height * width
            print("长方体的体积是:%.2f"% Volume)

    # 正方体
    def Cube(self,length):
        try:
            if length < 0 :
                raise PositiveIntegerError
        except Exception as e:
            print(e)
            logging.error("-----****棱长%d不合法***-----" % length, exc_info=True, stack_info=True)
        else:
            Volume = math.pow(length,3)
            print("正方体的体积是:%.2f" % Volume)

    # 圆柱体
    def Radius(self,radius,height):
        try:
            if radius < 0 or height < 0:
                raise PositiveIntegerError
        except Exception as e:
            if radius < 0:
                print(e)
                logging.error("-----****半径%d不合法***-----" % radius, exc_info=True, stack_info=True)
            if height < 0:
                print(e)
                logging.error("-----****高度%d不合法***-----" % height, exc_info=True, stack_info=True)
        else:
            S = math.pi * radius * radius
            Area = S * height
            print("圆柱体的体积为：%.3f"% Area)

if __name__ == '__main__':
    newShape = Cal_Voume()
    newShape.Radius(3,7)
    newShape.Radius(-3,-5)