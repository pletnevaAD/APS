class Buffer:
    def __init__(self, number):
        self.num_buff = number
        self.request = None
        self.under_sign = False

    def __str__(self):
        return "Номер буффера: " + str(self.num_buff) + "\nЗаявка: " + str(
            self.request) + "\nПод указателем " + str(self.under_sign) + "\n"
