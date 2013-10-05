__author__ = 'hiking'
__email__ = 'hikingko1@gmail.com'
from threading import Timer

class KitchenTimer:
    unit_time = 60
    lapse_time = 0
    threads = []
    def __init__(self, time):
        print "init"
        self.time = time

    def on_time_up(self): pass
    def on_each_minutes(self): pass
    def start(self):
        def __on_each_minutes():
            print "each"
            self.on_each_minutes()
            self.lapse_time += self.unit_time
            if(self.lapse_time >= self.unit_time * self.time):
                print "end"
                self.on_time_up()
            else:
                t_each = Timer(self.unit_time, __on_each_minutes, [])
                self.threads.append(t_each)
                t_each.start()
        t = Timer(self.unit_time, __on_each_minutes, [])
        self.threads.append(t)
        t.start()

    def join(self):
