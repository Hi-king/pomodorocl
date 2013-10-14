#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'hiking'
__email__ = 'hikingko1@gmail.com'

##==========##
## argument ##
##==========##
import argparse
import sys
class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)
class MyFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter): pass
parser = ArgumentParser(
    formatter_class=MyFormatter,
    description='''
=========================================================
Pomodoro Timer
=========================================================
''',
    epilog='''
=========================================================
''')
parser.add_argument('time', type=int)
parser.add_argument('--message')
parser.add_argument('--cal', help='name of the calendar to add log to')

##=========================
## Main
##=========================
import os
import time
import datetime
import os
from datetime import timedelta

sys.path.append(os.path.dirname(__file__))
print sys.path
from timer import KitchenTimer
from notifysend.notifysend import Notifier
from calendar_accessor import CalendarAccessor

class PomodoroCalendarAccessor(CalendarAccessor):
    def __init__(self, filename):
        CalendarAccessor.__init__(self, filename)
    def insert_event(self, calname, delta):
        end_time = datetime.datetime.utcfromtimestamp(time.time())
        start_time = end_time - timedelta(minutes=delta)
        start_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        end_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        CalendarAccessor.insert_event(self, calname, start_str, end_str)

class PomodoroTimer(KitchenTimer):
    def __init__(self, time, message="pomodoro finished"):
        KitchenTimer.__init__(self, time)
        self.message = message
        self.notifier = Notifier(message)
        self.accessor = PomodoroCalendarAccessor(os.environ['HOME']+"/.pomodoro")

    def on_each_minutes(self):
        print self.lapse_time

    def on_time_up(self):
        self.notifier.send()
        #time.sleep(60)
        self.accessor.insert_event("log", self.time)
        print self.message


def main(args):
    PomodoroTimer(args.time).start()

if __name__ == '__main__':
    args = parser.parse_args()
    print args
    main(args)
