from eventpubsub_client import eventpubsub_client
import asyncore
EVENT_PATH = "/"
EVENT_HOST = ""
EVENT_PORT = 8080

class event_cli(eventpubsub_client):
    def handle_call_status(self, data):
        print data

    def handle_init(self, data):
        print "wassup"

    def handle_start(self, data):
        print "incoming call from %s" % data['Caller']

    def handle_gather(self, data):
        # try:
        print "entered some digits %s" % data['Digits']
        # except:
            # pass
        
    def handle_end(self, data):
        print "caller hungup"

def run():
    event = event_cli(EVENTPUBSUB_HOST, EVENTPUBSUB_PORT, EVENTPUBSUB_PATH)
    asyncore.loop()

run()
