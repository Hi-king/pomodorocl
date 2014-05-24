__author__ = 'ogaki'

try:
    import pynotify
except ImportError:
    import pync

class Notifier:
    def __init__(self, message=""):
        try:
            _tmp = pynotify
            self.notifier = LinuxNotifier(message=message)
        except NameError:
            self.notifier = MacNotifier(message=message)

    def send(self):
        self.notifier.send()

class MacNotifier:
    """for Mac"""
    def __init__(self, message=""):
        self.message = message
    def send(self):
        pync.Notifier.notify(self.message)

class LinuxNotifier:
    """for Linux"""
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
