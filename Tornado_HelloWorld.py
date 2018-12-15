import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import socket
import json
import numpy as np
import time

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!!!")

class WebpageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        self.clients.add(self)
        print('[WS] New connection, ',len(self.clients),' client(s)')
        self.write_message(json.dumps(data_json))

    def on_message(self, message):
        m_json = json.loads(message)
        index = int(m_json["Name"][4:])
        data_json["DOut"][index-8] = m_json["Value"]
        
        [client.write_message(json.dumps(data_json)) for client in self.clients]
    
    def on_close(self):
        self.clients.remove(self)
        print('[WS] Connection closed, ',len(self.clients),' client(s)')

def make_app():
    settings = {
        'debug': True,
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    }
    handlers = [
        (r'/', MainHandler),
        (r'/webpage', WebpageHandler),
        (r'/ws', WebSocketHandler)
    ]
    return tornado.web.Application(handlers, **settings)

def updateJson():
    print("Update Json, elapsed time: ", time.time())
    for i in range(6):
        data_json["AIn"][i] = np.round(5*np.random.random(),5)


if __name__ == "__main__":
    print('Webserver started')
    print('Ip adress of server: ' + socket.gethostbyname(socket.gethostname()))

    with open('InitialInputs.json') as file:
        data_json = json.load(file) #Global variable

    app = make_app()
    app.listen(8888)
    tornado.ioloop.PeriodicCallback(updateJson,5000).start()
    tornado.ioloop.IOLoop.current().start()
#Press Ctrl + f5 to completely refresh site in Chrome