__author__ = 'hiking'
__email__ = 'hikingko1@gmail.com'

import os.path
import mox
import gdata.calendar.service
from unittest import TestCase
from calendar_accessor import CalendarAccessor


class TestCalendarAccessor(TestCase):
    dummy_filename = os.path.dirname(__file__)+"/sample.conf"

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_config(self):
        mock_calendar_service = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(gdata.calendar.service, 'CalendarService')
        gdata.calendar.service.CalendarService().AndReturn(mock_calendar_service)
        self.mox.StubOutWithMock(mock_calendar_service, 'ProgrammaticLogin')
        mock_calendar_service.ProgrammaticLogin()

        self.mox.ReplayAll()
        accessor = CalendarAccessor(TestCalendarAccessor.dummy_filename)
        self.assertEqual(accessor._email, "john@foo.com")
        self.assertEqual(accessor._password, 'abracadabra')
        self.mox.VerifyAll()
