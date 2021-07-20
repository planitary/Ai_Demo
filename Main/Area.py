import math, logging
from Error_info import *
from Log import LogConfig


class Cal_Area(BuildError):
    @classmethod
    def __init__(self):
        logging.info("Start")

    # 正方形面积
    def Square_Area(self, length):
        try:
            if length < 0:
                raise PositiveIntegerError
        except Exception as e:
            print(e)
            logging.error("-----****边长%d不合法***-----" % length, exc_info=True, stack_info=True)
        else:
            area = length * length
            print('正方形的面积是:%.2f' % area)

    # 矩形面积
    def Rectangle_Area(self, length_a, length_b):
        try:
            if length_b < 0 or length_a < 0:
                raise PositiveIntegerError
        except Exception as e:
            print(e)
            if length_b < 0:
                logging.error("-----****边长%d不合法***-----" % length_b, exc_info=True, stack_info=True)
            elif length_a < 0:
                logging.error("-----****边长%d不合法***-----" % length_a, exc_info=True, stack_info=True)
        else:
            area = length_a * length_b
            print('矩形的面积是:%.2f' % area)

    # 圆形面积
    def Circle_Area(self,radius):
        try:
            if radius < 0:
                raise PositiveIntegerError
        except Exception as e:
            print(e)
            logging.error("-----****半径%d不合法***-----" % radius, exc_info=True, stack_info=True)
        else:
            print('圆形的面积是:%.4f' % (math.pi * radius * radius))

    # 三角形面积
    def Triangle_Area(self, length_a, length_b, length_c):
        try:
            if (length_a + length_b > length_c and length_b + length_c > length_b and
                    length_a + length_c > length_b):
                # 海伦公式
                half_length = (length_a + length_b + length_c) / 2.0
                Area = math.sqrt(
                    half_length * (half_length - length_a) * (half_length - length_b) * (half_length - length_c))
                print("三角形面积为:%.2f" % Area)
            else:
                msg = '三角形'
                raise BuildError(msg)

        except Exception as e:
            print(e)
            logging.error("-----****边长%d %d %d不合法***-----" % (length_a, length_b, length_c),
                          exc_info=True, stack_info=True)


if __name__ == '__main__':
    newShape = Cal_Area()
    newShape.Circle_Area(-4)
    newShape.Rectangle_Area(23,44)
