from entity.device import Device


class Disciplines:
    def __init__(self):
        self.under_sign_num = None
        self.current_package = None
        self.current_request = None

    def request_selection(self, requests):
        if requests:
            if (self.current_package not in [request.num_source for request in requests]) or (
                    self.current_package is None):
                self.current_request = requests[0]
                self.current_package = requests[0].num_source
                for request in requests:
                    if request.num_source < self.current_request.num_source:
                        self.current_package = request.num_source
                        self.current_request = request
            for request in requests:
                if request.num_source == self.current_package:
                    if self.current_request is None:
                        self.current_request = request
                    elif request.num_request < self.current_request.num_request:
                        self.current_request = request
        else:
            self.current_request = None

    def set_on_device(self, devices, buffers, total_time) -> (Device, int):
        if self.current_request is not None:
            for device in devices:
                if device.is_free:
                    device.request = self.current_request
                    num_buf = 0
                    for buffer in buffers:
                        if buffer.request == self.current_request:
                            buffer.request = None
                            num_buf = buffer.num_buff
                    device.is_free = False
                    self.current_request = None
                    device.time = device.gen_time() + total_time
                    return device, num_buf

    def buffering(self, request, buffers, state, time):
        for index, buffer in enumerate(buffers):
            if buffer.under_sign:
                self.under_sign_num = index
        for i in range(self.under_sign_num):
            buffers.append(buffers.pop(i))
        for index, buffer in enumerate(buffers):
            if buffer.under_sign:
                buffer.under_sign = False
                if not buffer.request:
                    buffer.request = request
                    state['Источник'][buffer.num_buff] = request.num_source
                    state['Заявка'][buffer.num_buff] = request.num_request
                    state['Время'][buffer.num_buff] = round(time, 5)
                    if len(buffers) > index + 1:
                        buffers[index + 1].under_sign = True
                        print("1")
                    else:
                        buffers[0].under_sign = True
                        print("2")
                    break
                else:
                    if len(buffers) > index + 1:
                        buffers[index + 1].under_sign = True
                        print("3")
                    else:
                        if len(buffers) > 1:
                            buffers[1].under_sign = True
                        else:
                            buffers[0].under_sign = True
                        print("4")
                        failed_req = buffers[0].request
                        buffers[0].request = request
                        state['Источник'][buffers[0].num_buff] = request.num_source
                        state['Заявка'][buffers[0].num_buff] = request.num_request
                        state['Время'][buffer.num_buff] = round(time, 5)
                        return failed_req
