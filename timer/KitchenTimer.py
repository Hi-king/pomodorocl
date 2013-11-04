__author__ = 'hiking'
__email__ = 'hikingko1@gmail.com'
from threading import Timer


class KitchenTimer:
    def __init__(self, time):
        self.unit_time = 60
        self.lapse_time = 0
        self.threads = []
        self.time = time

    def on_time_up(self): pass
    def on_each_minutes(self): pass
    def start(self):
        def __on_each_minutes():
            self.on_each_minutes()
            self.lapse_time += self.unit_time
            if self.lapse_time >= self.unit_time * self.time:
                self.on_time_up()
            else:
                t_each = Timer(self.unit_time, __on_each_minutes, [])
                self.threads.append(t_each)
                t_each.start()
        t = Timer(self.unit_time, __on_each_minutes, [])
        self.threads.append(t)
        t.start()

    def join(self):
        while len(self.threads) < self.time:
            for each_thread in self.threads:
                if each_thread.is_alive():
                    each_thread.join(self.unit_time)
        for each_thread in self.threads:
            if each_thread.is_alive():
                each_thread.join(self.unit_time)
        print "end",len(self.threads),self.time