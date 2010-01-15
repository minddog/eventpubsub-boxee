from twilio_event_client import twilio_event
import asyncore
# EVENT_URL = '/2008-08-01/Accounts/*?sid=AC835bd998c432f1a1907789f75e350c03&auth=mbMDHIlrl68%2B85nyp6ceG1C7vDc%3D'
EVENT_URL = '/2008-08-01/Accounts/AC699e22140410f059a02bd01c1950cfd2/*?sid=AC699e22140410f059a02bd01c1950cfd2&auth=fYRmqxbWK21aXjD1ogL2rsxcbIM%3D'


class cli_twilio_event(twilio_event):
    def handle_call_status(self, data):
        print data

    def handle_init(self, data):
        print "wassup"

    def handle_start(self, data):
        print "incoming call from %s" % data['Caller']

    def handle_gather(self, data):
        print "entered some digits %s" % data['Digits']

    def handle_end(self, data):
        print "caller hungup"

def run():
    event = cli_twilio_event('events.twilio.com', EVENT_URL)
    asyncore.loop()
