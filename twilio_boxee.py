from eventpubsub_client import eventpubsub_client
import asyncore
import mc
import simplejson as json

EVENTPUBSUB_PATH = "/"
EVENTPUBSUB_HOST = "blackacid.org"
EVENTPUBSUB_PORT = 8080

BOXEE_WEB_PATH = "/Applications/Boxee.app/Contents/Resources/Boxee/web"

class boxee_twilio_event(eventpubsub_client):
    def handle_call_status(self, data):
        print data
        if 'in-progress' in data['CallStatus']:
            mc.ShowDialogNotification("Call in progress with %s." % "test")
            print "caller hungup"

    def handle_init(self, data):
        pass

    def handle_end(self, data):
        pass
    
    def handle_start(self, data):
        message = str("incoming call from " + data["Caller"])
        mc.ShowDialogNotification(message)
        print message

    def _update_playerinfo(self, mc):
        player = mc.GetPlayer()
        item = player.GetPlayingItem()
        print item.GetTitle()
        item_json = json.dumps(item.Dump())
        item_file = open(BOXEE_WEB_PATH + "/playerItem.json", "w+")
        item_file.write(item_json)
        item_file.close()
        
def run():
    event = boxee_twilio_event(EVENTPUBSUB_HOST, EVENTPUBSUB_PORT, EVENTPUBSUB_PATH)
    asyncore.loop()
