__author__ = 'ogaki'

import os
from unittest import TestCase
from calendar_accessor import CalendarAccessor

class TestCalendarAccessorConnection(TestCase):
    def test_show_calendars(self):
        """show calendars using real connection"""
        calendar_accessor = CalendarAccessor(os.environ['HOME']+"/.pomodoro")
        calendars = calendar_accessor.get_calendars()
        self.assertIsInstance(calendars, list)
        print calendars
