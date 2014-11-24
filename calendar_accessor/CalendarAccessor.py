#!/usr/bin/python
import gdata.calendar
import gdata.calendar.service
import gdata.calendar.data
import gdata.calendar.client
import atom
import ConfigParser
import oauth2client.client
import oauth2client.tools
import oauth2client.file
import apiclient.discovery
import httplib2
import os


class CalendarAccessor:
    """
    @see http://taichino.com/programming/python-programming/3101
    @see https://developers.google.com/api-client-library/python/start/get_started#simple
    """
    def __init__(self, conf_filename, authorization_cache_filename=os.environ['HOME']+"/.pomodoro.auth"):
        self.parser = ConfigParser.SafeConfigParser()
        self.__parse_config(conf_filename)
        self.connection = self.__get_authorized_connection(authorization_cache_filename)
        self.calendar_service = apiclient.discovery.build('calendar', 'v3', http=self.connection)

    def __get_authorized_connection(self, cache_filename):
        storage = oauth2client.file.Storage(cache_filename)
        credentials = storage.get()
        if not credentials or credentials.invalid:
            flow = oauth2client.client.OAuth2WebServerFlow(
                client_id=self._client_id,
                client_secret=self._client_secret,
                scope=['https://www.googleapis.com/auth/calendar'],
                user_agent='pomodorocl'
            )
            credentials = oauth2client.tools.run(
                flow,
                storage
            )
        http = httplib2.Http()
        credentials.authorize(http)
        return http

    def __parse_config(self, filename):
        self.parser.read(filename)
        argdict = dict(self.parser.items(self.parser.sections()[0]))
        try:
            self._client_id = argdict['client_id']
            self._client_secret = argdict['client_secret']
        except:
            print "error parse config %s " % filename
            raise

    def get_calendars(self):
        calendars = self.calendar_service.calendarList().list().execute()
        return [{'id': calendar['id'], 'summary': calendar['summary']} for calendar in calendars['items']]

    def insert_event(self, calname, start, end, title="event"):
        calendars = self.calendar_service.calendarList().list().execute()
        for eachcal in calendars['items']:
            if eachcal['summary'] == calname:
                cal = eachcal
                break
        else:
            print "Calendar %s not found" % calname
            raise Exception("Calendar %s not found" % calname)

        event = {
            'start': {'dateTime': start},
            'end':   {'dateTime': end},
            'summary': title
        }
        target_calendar_id = cal['id']
        created_event = self.calendar_service.events().insert(calendarId=target_calendar_id, body=event).execute()
        print created_event['htmlLink']
        print "event insert done"


class CalendarAccessorV2:
    def __init__(self, filename):
        self.parser = ConfigParser.SafeConfigParser()
        self.__parse_config(filename)
        # self.calendar_service = gdata.calendar.service.CalendarService()
        # self.calendar_service.email = self._email
        # self.calendar_service.password = self._password
        # self.calendar_service.ProgrammaticLogin()
        self.calendar_client = gdata.calendar.client.CalendarClient(source="hiking-pomodoro-v1")
        self.calendar_client.client_login(self._email, self._password, self.calendar_client.source)

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
        result = self.calendar_client.InsertEvent(event, cal.content.src)
        # result = self.calendar_service.InsertEvent(event, cal.content.src)
        print result.GetEditLink().href
        print result.GetHtmlLink().href

    def get_calendars(self):
        return self.calendar_client.GetAllCalendarsFeed()

    def show_events(self):
        return self.calendar_service.GetCalendarListEntry("log")
