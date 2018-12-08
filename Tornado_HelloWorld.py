import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import socket
import xml.etree.ElementTree as ET
import re

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!!!")

class WebpageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class XMLHandler(tornado.web.RequestHandler):
    def prepare(self):
        for i,elem in enumerate(root.iter('DOut')):
            if self.get_query_arguments('DOut' + str(i+8)) != []:
                print('DOut' + str(i+8) + '=' + str(self.get_query_argument('DOut' + str(i+8))))
                if self.get_query_argument('DOut' + str(i+8)) == 'true':
                    elem.text = 'High'
                else:
                    elem.text = 'Low'
    def get(self,fname):
        self.set_header("Content-Type", "text/xml")
        self.write(ET.tostring(root))

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        self.clients.add(self)
        print('[WS] New connection, ',len(self.clients),' client(s)')
        self.write_message(ET.tostring(root))

    def on_message(self, message):
        index = [int(i) for i in re.findall(r'\d+', message)][0]
        if message.find('true') >= 0:
            root[2][index-8].text = 'High'
        else:
            root[2][index-8].text = 'Low'
        
        [client.write_message(ET.tostring(root)) for client in self.clients]
    
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

    tree = ET.parse('InitialInputs.xml') #Global variables
    root = tree.getroot()

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

#Press Ctrl + f5 to completely refresh site in Chrome