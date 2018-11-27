import os
import tornado.ioloop
import tornado.web
import socket

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!!!")

class WebpageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

def make_app():
    settings = {
        'debug': True,
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    }
    handlers = [
        (r'/', MainHandler),
        (r'/webpage', WebpageHandler),
        (r'/(ajaxInputs_random.xml)', tornado.web.StaticFileHandler, {'path': ''})
    ]
    return tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    print('Webserver started')
    print('Ip adress of server: ' + socket.gethostbyname(socket.gethostname()))
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

#Press Ctrl + f5 to refresh favicon