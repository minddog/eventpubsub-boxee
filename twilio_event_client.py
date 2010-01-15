import re, string

import asyncore
import socket
import cgi 

EXTRACT_EVENT_EXPR = "^.*temsg\(\"(?P<name>[a-zA-Z-_0-9/]*)\", \"(?P<value>.*)\"\).*$"
class twilio_event(asyncore.dispatcher_with_send):
    def __init__(self, host, path):
        asyncore.dispatcher_with_send.__init__(self)

        self.host = host
        self.path = path

        self.header = None

        self.data = ""

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, 80))

    def handle_connect(self):
        # connection succeeded; send request
        self.send(
            "GET %s HTTP/1.0\r\nHost: %s\r\n\r\n" %
                (self.path, self.host)
            )

    def handle_expt(self):
        # connection failed
        self.close()

    def handle_read(self):
        # deal with incoming data
        data = self.recv(4096)
        
        if not self.header:
            self.data = self.data + data

            try:
                i = string.index(self.data, "\r\n\r\n")
            except ValueError:
                return

            self.header = self.data[:i+2]

            data = self.data[i+4:]
            self.data = ""

        if data and len(data.strip()) != 0:
            try:
                result = re.findall(EXTRACT_EVENT_EXPR, data, re.MULTILINE)
                [self.handle_event(method, data) for method, data in result]
            except AttributeError, e:
                print "Error processing data %s: %s" % (data, e)

            
            # print self.host, "DATA", len(data)

    def handle_event(self, name, value):
        print name
        value = cgi.parse_qs(value)
        try:
            event = {'all': self.handle_init,
                     'twilio-call/info': self.handle_info,
                     'twilio-gather/end': self.handle_gather,
                     'twilio-call/start' : self.handle_start,
                     'twilio-call/end' : self.handle_end,
                     }[name](value)
        except KeyError, e:
            print "Event not supported yet."

    def handle_close(self):
        self.close()

    def handle_info(self, data):
        self.handle_call_status(data)
            
    # Implement these in a subclass
    def handle_call_status(self, data):
        pass

    def handle_init(self, data):
        pass

    def handle_start(self, data):
        pass

    def handle_gather(self, data):
        pass
