import heapq
from pprint import pprint

from disciplines.disciplines import Disciplines
from entity.buffer import Buffer
from entity.device import Device
from entity.request import Request
from entity.source import Source


class SMO:
    def __init__(self, source_amount, request_amount, buffers_amount, devices_amount):
        self.source_amount = source_amount
        self.request_amount = request_amount
        self.buffers_amount = buffers_amount
        self.devices_amount = devices_amount
        self.total_time = 0
        self.sources = [Source(i, 0.2) for i in range(source_amount)]
        self.buffers = [Buffer(i) for i in range(buffers_amount)]
        self.devices = [Device(i, 1, 10) for i in range(devices_amount)]
        self.queue_source = []
        self.queue_device = []
        self.buffers[0].under_sign = True
        self.discipline = Disciplines()
        self.current_state = dict.fromkeys(['Событие', 'Время', 'Признак', 'Число заявок', 'Число отказов'])
        self.current_state['Событие'] = ["И" + str(i) for i in range(source_amount)] \
                                        + ["П" + str(i) for i in range(devices_amount)]
        self.current_state['Время'] = [0 for i in range(source_amount + devices_amount)]
        self.current_state['Число заявок'] = [0 for i in range(source_amount)] + ["-" for i in range(devices_amount)]
        self.current_state['Число отказов'] = [0 for i in range(source_amount)] + ["-" for i in range(devices_amount)]
        self.current_state['Признак'] = ["-" for i in range(devices_amount + source_amount)]
        self.current_state_buf = dict.fromkeys(['Позиция', 'Время', 'Источник', 'Заявка'])
        self.current_state_buf['Позиция'] = ["Б" + str(i) for i in range(buffers_amount)]
        self.current_state_buf['Источник'] = ["-" for i in range(buffers_amount)]
        self.current_state_buf['Заявка'] = ["-" for i in range(buffers_amount)]
        self.current_state_buf['Время'] = [0 for i in range(buffers_amount)]
        self.source_charact = dict.fromkeys(
            ['Источник', 'Количество заявок', 'Вероятность отказа', 'Тпреб', 'TБП', 'Tобсл', 'ДБП', 'Добсл'])
        self.source_charact['Источник'] = ["И" + str(i) for i in range(source_amount)]
        self.source_charact['Вероятность отказа'] = [0 for i in range(source_amount)]
        self.source_charact['Количество заявок'] = [0 for i in range(source_amount)]
        self.source_charact['Tобсл'] = [0 for i in range(source_amount)]
        self.source_charact['Тпреб'] = [0 for i in range(source_amount)]
        self.source_charact['TБП'] = [0 for i in range(source_amount)]
        self.source_charact['ДБП'] = [0 for i in range(source_amount)]
        self.source_charact['Добсл'] = [0 for i in range(source_amount)]
        self.device_charact = dict.fromkeys(['Прибор', 'Коэффициент использования'])
        self.device_charact['Прибор'] = ["П" + str(i) for i in range(devices_amount)]
        self.device_charact['Коэффициент использования'] = [0 for i in range(devices_amount)]
        self.devices_request_amount = [0 for i in range(devices_amount)]
        for i in range(source_amount):
            time = self.sources[i].gen_time()
            request = Request(self.sources[i].num_source, 0, time)
            heapq.heappush(self.queue_source, request)

    def iteration(self):
        for i in range(self.source_amount):
            self.current_state['Признак'][i] = "-"
        print(self.current_state)
        for device in self.devices:
            if device.request:
                self.current_state['Признак'][self.source_amount + device.num_device] = f"Обслуживание заявки " \
                                                                                        f"{device.request.num_source}" \
                                                                                        f".{device.request.num_request}"
            else:
                self.current_state['Признак'][self.source_amount + device.num_device] = "-"
        if self.queue_source and ((not self.queue_device) or (self.queue_device[0].time > self.queue_source[0].time)):
            request = heapq.heappop(self.queue_source)
            self.current_state['Время'][request.num_source] = round(request.time, 5)
            self.current_state['Число заявок'][request.num_source] += 1
            for i in range(self.source_amount + self.devices_amount):
                if i == request.num_source:
                    self.current_state['Признак'][i] = "Сгенерировал заявку"
            self.request_amount -= 1
            if self.request_amount == 0:
                print("im here")
                self.queue_source.clear()
                print(self.queue_source)
            failed_req = self.discipline.buffering(request, self.buffers, self.current_state_buf, request.time)
            self.source_charact['TБП'][request.num_source] -= request.time
            if failed_req:
                print("________")
                self.current_state['Число отказов'][failed_req.num_source] += 1
                self.source_charact['TБП'][failed_req.num_source] += request.time
            self.total_time = request.time
            if True in [device.is_free for device in self.devices]:
                self.discipline.request_selection([buffer.request for buffer in self.buffers if buffer.request])
                device_buf = self.discipline.set_on_device(self.devices, self.buffers, self.total_time)
                if device_buf is not None:
                    print(device_buf)
                    heapq.heappush(self.queue_device, device_buf[0])
                    self.current_state['Признак'][self.source_amount + device_buf[0].num_device] = \
                        f"Постановка заявки {device_buf[0].request.num_source}" \
                        f".{device_buf[0].request.num_request} на обслуживание"
                    self.source_charact['Tобсл'][device_buf[0].request.num_source] -= self.total_time
                    self.source_charact['TБП'][device_buf[0].request.num_source] += self.total_time
                    self.device_charact['Коэффициент использования'][device_buf[0].num_device] -= self.total_time
                    self.current_state_buf['Источник'][device_buf[1]] = "-"
                    self.current_state_buf['Заявка'][device_buf[1]] = "-"
                    self.current_state_buf['Время'][device_buf[1]] = round(self.total_time, 5)
                    self.current_state['Время'][self.source_amount + device_buf[0].num_device] = round(self.total_time,
                                                                                                       5)
            if self.request_amount != 0:
                for i in range(len(self.sources)):
                    if self.sources[i].num_source == request.num_source:
                        time = self.sources[i].gen_time()
                        new_request = Request(i, request.num_request + 1, time + self.total_time)
                        heapq.heappush(self.queue_source, new_request)
        else:
            device = heapq.heappop(self.queue_device)
            self.current_state['Время'][self.source_amount + device.num_device] = round(device.time, 5)
            for i in range(self.source_amount + self.devices_amount):
                if i == self.source_amount + device.num_device:
                    self.current_state['Признак'][i] = f"Конец обслуживания заявки {device.request.num_source}" \
                                                       f".{device.request.num_request}"
                    self.source_charact['Tобсл'][device.request.num_source] += device.time
                    self.device_charact['Коэффициент использования'][device.num_device] += device.time
                    self.devices_request_amount[device.num_device] += 1
            device.is_free = True
            device.request = None
            self.total_time = device.time
            if True in [device.is_free for device in self.devices]:
                self.discipline.request_selection([buffer.request for buffer in self.buffers if buffer.request])
                device_buf = self.discipline.set_on_device(self.devices, self.buffers, self.total_time)
                if device_buf is not None:
                    heapq.heappush(self.queue_device, device_buf[0])
                    self.current_state['Признак'][self.source_amount + device_buf[
                        0].num_device] += f" => Постановка заявки {device_buf[0].request.num_source}" \
                                          f".{device_buf[0].request.num_request} на обслуживание"
                    self.source_charact['Tобсл'][device_buf[0].request.num_source] -= self.total_time
                    self.source_charact['TБП'][device_buf[0].request.num_source] += self.total_time
                    self.device_charact['Коэффициент использования'][device_buf[0].num_device] -= self.total_time
                    self.current_state_buf['Источник'][device_buf[1]] = "-"
                    self.current_state_buf['Заявка'][device_buf[1]] = "-"
                    self.current_state_buf['Время'][device_buf[1]] = round(self.total_time, 5)
                    self.current_state['Время'][self.source_amount + device_buf[0].num_device] = round(self.total_time,
                                                                                                       5)

    def all_iteration(self):
        device_times = [[] for i in range(self.source_amount)]
        buf_times = [[] for i in range(self.source_amount)]
        while True:
            if self.queue_source or self.queue_device:
                self.iteration()
                for i in range(self.source_amount):
                    device_total_time = 0
                    buf_total_time = 0
                    for j in range(len(device_times[i])):
                        device_total_time += device_times[i][j]
                    for j in range(len(buf_times[i])):
                        buf_total_time += buf_times[i][j]
                    if self.source_charact['Tобсл'][i] > device_total_time:
                        device_times[i].append(self.source_charact['Tобсл'][i] - device_total_time)
                    if self.source_charact['TБП'][i] > buf_total_time:
                        buf_times[i].append(self.source_charact['TБП'][i] - buf_total_time)
            else:
                for i in range(self.source_amount):
                    if self.current_state['Число отказов'][i]:
                        self.source_charact['Вероятность отказа'][i] = self.current_state['Число отказов'][i] / \
                                                                       self.current_state['Число заявок'][i]
                    self.source_charact['Количество заявок'][i] = self.current_state['Число заявок'][i]
                    if self.source_charact['Количество заявок'][i]:
                        self.source_charact['Tобсл'][i] /= self.source_charact['Количество заявок'][i]
                        self.source_charact['TБП'][i] /= self.source_charact['Количество заявок'][i]
                        self.source_charact['Тпреб'][i] = self.source_charact['Tобсл'][i] + \
                                                          self.source_charact['TБП'][i]
                    for j in range(len(device_times[i])):
                        self.source_charact['Добсл'][i] += (device_times[i][j] - self.source_charact['Tобсл'][i])
                    for j in range(len(buf_times[i])):
                        self.source_charact['ДБП'][i] += (buf_times[i][j] - self.source_charact['TБП'][i])
                    if self.source_charact['Количество заявок'][i]:
                        self.source_charact['Добсл'][i] /= self.source_charact['Количество заявок'][i]
                        self.source_charact['ДБП'][i] /= self.source_charact['Количество заявок'][i]
                for i in range(self.devices_amount):
                    self.device_charact['Коэффициент использования'][i] /= self.total_time
                return
