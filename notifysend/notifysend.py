__author__ = 'ogaki'

import pynotify

class Notifier:
    def __init__(self, message=""):
        pynotify.init(message)
        self.n = pynotify.Notification(message, message)
        self.n.add_action("default", "default action", self.on_accepted)
        self.n.connect('closed', self.on_declined)
    def send(self):
        self.n.show()
    def on_accepted(self):
        print "accepted"
    def on_declined(self):
        print "declined"