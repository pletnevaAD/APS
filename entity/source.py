import math
import random


class Source:
    def __init__(self, number, speed):
        self.num_source = number
        self.speed = speed

    def gen_time(self):
        time = (-1 / self.speed) * math.log(random.random())
        return time
