import sys,os
sys.path.append(os.path.abspath(os.path.dirname('__file__')))

import re, string

import asyncore
import socket
import cgi 
import simplejson as json


class twilio_event(asyncore.dispatcher_with_send):
    def __init__(self, host, port, path):
        asyncore.dispatcher_with_send.__init__(self)

        self.host = host
        self.path = path
        self.port = port
        
        self.header = None

        self.data = ""

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

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
                print data
                result = json.loads(data)
                if result:
                    try:
                        [self.handle_event(method, result[method]) for method in result.keys()]
                    except ValueError, e:
                        pass
                    
            except AttributeError, e:
                print "Error processing data %s: %s" % (data, e)

            
            # print self.host, "DATA", len(data)

    def handle_event(self, name, value):
        print name
        print value
        # value = cgi.parse_qs(value)
        # print value
        try:
            value = json.loads(value[0])
            print value
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
