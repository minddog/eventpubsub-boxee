from twisted.internet import reactor, task
from twisted.web.server import Site
from twisted.web import server
from twisted.web.resource import Resource

import time
import json

EVENTPUBSUB_PORT = 8080

class EventPubSub(Resource):
    isLeaf = True
    def __init__(self):
        self.presence=[]
        loopingCall = task.LoopingCall(self.__keep_alive)
        loopingCall.start(100, False)
        Resource.__init__(self)

    def render_GET(self, request):
        request.write(json.dumps('init'))
        self.presence.append(request)
        return server.NOT_DONE_YET

    def render_POST(self, request):
        request.write(json.dumps("success"))
        payload = json.dumps(request.args)
        for p in self.presence:
            p.write("%s\r\n" % payload)
        return 'success'
    
    def __keep_alive(self):
        payload = json.dumps('keep-alive')
        for p in self.presence:
            p.write('%s\r\n' % payload)
            
resource = EventPubSub()
factory = Site(resource)
reactor.listenTCP(EVENTPUBSUB_PORT, factory)
reactor.run()
