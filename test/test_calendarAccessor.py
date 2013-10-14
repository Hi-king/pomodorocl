__author__ = 'hiking'
__email__ = 'hikingko1@gmail.com'

import os.path
from unittest import TestCase
from calendar_accessor import CalendarAccessor


class TestCalendarAccessor(TestCase):
    dummy_filename = os.path.dirname(__file__)+"/sample.conf"

    def test_config(self):
        accessor = CalendarAccessor(TestCalendarAccessor.dummy_filename)
        self.assertEqual(accessor._email, "john@foo.com")
        self.assertEqual(accessor._password, 'abracadabra')
