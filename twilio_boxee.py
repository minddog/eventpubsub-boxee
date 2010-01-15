from twilio_event_client import twilio_event
import asyncore
import mc
# EVENT_URL = '/2008-08-01/Accounts/*?sid=AC835bd998c432f1a1907789f75e350c03&auth=mbMDHIlrl68%2B85nyp6ceG1C7vDc%3D'
EVENT_URL = '/2008-08-01/Accounts/AC699e22140410f059a02bd01c1950cfd2/*?sid=AC699e22140410f059a02bd01c1950cfd2&auth=fYRmqxbWK21aXjD1ogL2rsxcbIM%3D'


class boxee_twilio_event(twilio_event):
    def handle_call_status(self, data):
        print data
        if 'in-progress' in data['CallStatus']:
            mc.ShowDialogNotification("Call in progress with %s." % data['Caller'])
            print "caller hungup"

    def handle_init(self, data):
        print "wassup"

    def handle_start(self, data):
        mc.ShowDialogNotification("An incoming call from %s." % data['Caller'])
        try:
            player = mc.GetPlayer()
            player.pause()
        except: # TODO FIX ME when not falling asleep
            pass
        print "incoming call from %s" % data['Caller']

    def handle_gather(self, data):
        mc.ShowDialogNotification("Gathered: %s." % data['Digits'])
        print "entered some digits %s" % data['Digits']

    def handle_end(self, data):
        try:
            player = mc.GetPlayer()
            player.play()
        except:
            pass
        mc.ShowDialogNotification("Caller %s disconnected." % data['Caller'])
        print "caller hungup"

def run():
    event = boxee_twilio_event('events.twilio.com', EVENT_URL)
    asyncore.loop()
