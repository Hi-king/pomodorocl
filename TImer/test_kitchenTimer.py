from unittest import TestCase
from KitchenTimer import KitchenTimer

__author__ = 'ogaki'


class TestKitchenTimer(TestCase):
    def test_all_finish(self):
        '''Have threads been finished?'''
        kitchentimer = KitchenTimer(5)
        kitchentimer.unit_time = 0.1
        kitchentimer.start()
        while(len(kitchentimer.threads) < 5):
            for each_thread in kitchentimer.threads:
                if each_thread.is_alive():
                    each_thread.join(1)
        self.assertEqual(len(kitchentimer.threads), 5)

    def test_on_each_minutes(self):
        '''on_each_minutes method'''
        kitchentimer = KitchenTimer(5)
        kitchentimer.unit_time = 0.1
        self.o=0
        def tmp_each_minutes():
            self.o += 1
        kitchentimer.on_each_minutes = tmp_each_minutes
        kitchentimer.start()
        while(len(kitchentimer.threads) < 5):
            for each_thread in kitchentimer.threads:
                if each_thread.is_alive():
                    each_thread.join(1)
        for each_thread in kitchentimer.threads:
            if each_thread.is_alive():
                each_thread.join(1)
        self.assertEqual(self.o, 5)