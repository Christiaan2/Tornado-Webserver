import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import socket
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!!!")

class WebpageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class XMLHandler(tornado.web.RequestHandler):
    def prepare(self):
        for i,elem in enumerate(data_json["DOut"]):
            if self.get_query_arguments('DOut' + str(i+8)) != []:
                print('DOut' + str(i+8) + '=' + str(self.get_query_argument('DOut' + str(i+8))))
                if self.get_query_argument('DOut' + str(i+8)) == 'true':
                    elem = 'High'
                else:
                    elem = 'Low'
    def get(self,fname):
        #self.set_header("Content-Type", "text/xml")
        self.write(json.dumps(data_json))

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        self.clients.add(self)
        print('[WS] New connection, ',len(self.clients),' client(s)')
        self.write_message(json.dumps(data_json))

    def on_message(self, message):
        m_json = json.loads(message)
        index = int(m_json["Name"][4:])
        if m_json["Value"]:
            data_json["DOut"][index-8] = 'High'
        else:
            data_json["DOut"][index-8] = 'Low'
        
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
        (r'/(ajaxInputs_random.xml)', XMLHandler),
        (r'/ws', WebSocketHandler)
    ]
    return tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    print('Webserver started')
    print('Ip adress of server: ' + socket.gethostbyname(socket.gethostname()))

    with open('InitialInputs.json') as file:
        data_json = json.load(file) #Global variable

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

#Press Ctrl + f5 to completely refresh site in Chrome