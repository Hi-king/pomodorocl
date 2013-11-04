#!/usr/bin/python
import gdata.calendar
import gdata.calendar.service
import gdata.calendar.data
import atom
import ConfigParser


class CalendarAccessor:
    def __init__(self, filename):
        self.parser = ConfigParser.SafeConfigParser()
        self.__parse_config(filename)
        self.calendar_service = gdata.calendar.service.CalendarService()
        self.calendar_service.email = self._email
        self.calendar_service.password = self._password
        self.calendar_service.ProgrammaticLogin()

    def __parse_config(self, filename):
        self.parser.read(filename)
        argdict = dict(self.parser.items(self.parser.sections()[0]))
        try:
            self._email = argdict['email']
            self._password = argdict['password']
        except:
            print "error parse config %s " % filename
            raise

    def insert_event(self, calname, start, end, title="event"):

        for eachcal in self.calendar_service.GetOwnCalendarsFeed().entry:
            if eachcal.title.text == calname:
                cal = eachcal
                break
        else:
            print "Calendar %s not found" % calname
            raise Exception("Calendar %s not found" % calname)


        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=title)
        event.content = atom.Content(text="test content")
        event.when.append(gdata.calendar.When(start_time=start, end_time=end))
        result = self.calendar_service.InsertEvent(event, cal.content.src)
        print result.GetEditLink().href
        print result.GetHtmlLink().href
