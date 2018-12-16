import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import socket
import json
import numpy as np
import time
import sys

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        self.clients.add(self)
        print('[WS] New connection, ',len(self.clients),' client(s)')
        self.write_message(IOHandler.__str__())

    def on_message(self, message):
        IOHandler.updateOutput(message)
        self.update_clients()
    
    def on_close(self):
        self.clients.remove(self)
        print('[WS] Connection closed, ',len(self.clients),' client(s)')

    @classmethod
    def update_clients(cls):
        [client.write_message(IOHandler.__str__()) for client in cls.clients]

class IOHandler():
    def __init__(self):
        sys.exit('ERROR: IOHandler instance should NOT be created')
    
    @classmethod
    def initialize(cls):
        with open('InitialInputs.json') as file:
            cls.data_json = json.load(file)
        cls.prev_time = time.time()
        tornado.ioloop.PeriodicCallback(cls.updateJson,5000).start()
    
    @classmethod
    def updateJson(cls):
        cur_time = time.time()
        print("Update json, elapsed time: ", cur_time-cls.prev_time)
        cls.prev_time = cur_time
        for i in range(len(cls.data_json["AIn"])):
            cls.data_json["AIn"][i] = np.round(5*np.random.random(),5)
        for i in range(len(cls.data_json["DIn"])):
            cls.data_json["DIn"][i] = np.random.random() > 0.5
        WebSocketHandler.update_clients()

    @classmethod
    def updateOutput(cls, message):
        m_json = json.loads(message)
        index = int(m_json["Name"][4:])
        cls.data_json["DOut"][index-8] = m_json["Value"]
    
    @classmethod
    def __str__(cls):
        return json.dumps(cls.data_json)

def make_app():
    settings = {
        'debug': True,
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    }
    handlers = [
        (r'/', MainHandler),
        (r'/ws', WebSocketHandler)
    ]
    return tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)

    IOHandler.initialize()

    print('Webserver started')
    print('Ip adress of server: ' + socket.gethostbyname(socket.gethostname()))
    tornado.ioloop.IOLoop.current().start()

#Press Ctrl + f5 to completely refresh site in Chrome