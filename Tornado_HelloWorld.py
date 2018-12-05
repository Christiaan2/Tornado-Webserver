import os
import tornado.ioloop
import tornado.web
import socket
import xml.etree.ElementTree as ET

tree = ET.parse('ajaxInputs_random.xml')
root = tree.getroot()

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

def make_app():
    settings = {
        'debug': True,
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    }
    handlers = [
        (r'/', MainHandler),
        (r'/webpage', WebpageHandler),
        (r'/(ajaxInputs_random.xml)', XMLHandler)
    ]
    return tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    print('Webserver started')
    print('Ip adress of server: ' + socket.gethostbyname(socket.gethostname()))
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

#Press Ctrl + f5 to completely refresh site in Chrome