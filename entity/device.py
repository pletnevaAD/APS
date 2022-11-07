import random


class Device:
    def __init__(self, number, min_time, max_time):
        self.num_device = number
        self.min_time = min_time
        self.max_time = max_time
        self.request = None
        self.time = None
        self.is_free = True

    def gen_time(self):
        time = random.uniform(self.min_time, self.max_time)
        return time

    def __lt__(self, nxt):
        return self.time < nxt.time

    def __str__(self):
        return "Номер прибора: " + str(self.num_device) + "\nЗаявка: " + str(
            self.request) + "\nВремя: " + str(self.time) + "\nСвободен: " + str(self.is_free)+"\n"
