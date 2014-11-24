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
parser.add_argument('--message', default="pomodoro")
parser.add_argument('--cal', required=True, help='name of the calendar to add log to')

##=========================
## Main
##=========================
import os
import time
import datetime
from datetime import timedelta

sys.path.append(os.path.dirname(__file__))
print sys.path
from timer import KitchenTimer
from notifysend.notifysend import Notifier
from calendar_accessor import CalendarAccessor

class PomodoroCalendarAccessor(CalendarAccessor):
    def __init__(self, filename):
        CalendarAccessor.__init__(self, filename)
    def insert_event(self, calname, delta, title="pomodoro"):
        end_time = datetime.datetime.utcfromtimestamp(time.time())
        start_time = end_time - timedelta(minutes=delta)
        start_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        end_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        # start_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
        # end_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
        CalendarAccessor.insert_event(self, calname, start_str, end_str, title=title)

class PomodoroTimer(KitchenTimer):
    def __init__(self, time, calname, message="pomodoro"):
        KitchenTimer.__init__(self, time)
        self.message = message
        self.calname = calname
        self.notifier = Notifier(message)
        self.accessor = PomodoroCalendarAccessor(os.environ['HOME']+"/.pomodoro")

    def on_each_minutes(self):
        print self.lapse_time / self.unit_time

    def on_time_up(self):
        self.notifier.send()
        #time.sleep(60)
        self.accessor.insert_event(self.calname, self.time, self.message)
        print self.message


def main(args):
    if args.message:
        timer = PomodoroTimer(args.time, args.cal, message=args.message)
    else:
        timer = PomodoroTimer(args.time, args.cal)
    timer.start()

if __name__ == '__main__':
    args = parser.parse_args()
    print args
    main(args)
