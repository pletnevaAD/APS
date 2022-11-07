class Request:
    def __init__(self, num_source, num_request, time):
        self.num_source = num_source
        self.num_request = num_request
        self.time = time

    def __lt__(self, nxt):
        return self.time < nxt.time

    def __str__(self):
        return "Номер источника: " + str(self.num_source) + "\nНомер заявки: " + str(
            self.num_request) + "\nВремя: " + str(self.time) + "\n"
