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
sys.path.append(os.path.dirname(__file__))
print sys.path
from Timer import KitchenTimer


class PomodoroTimer(KitchenTimer):
    def __init__(self, time, message="pomodoro finished"):
        KitchenTimer.__init__(self, time)
        self.message = message

    def on_time_up(self):
        print self.message


def main(args):
    PomodoroTimer(args.time).start()

if __name__ == '__main__':
    args = parser.parse_args()
    print args
    main(args)
