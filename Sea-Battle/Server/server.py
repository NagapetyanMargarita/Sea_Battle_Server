# import cgi
# from http.server import HTTPServer, BaseHTTPRequestHandler
# import socketserver
#
# import json
#
#
# class Server(BaseHTTPRequestHandler):
#     def _set_headers(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#
#     def do_HEAD(self):
#         self._set_headers()
#
#     # GET sends back a Hello world message
#     def do_GET(self):
#         data = json.load(open('data.json', 'r', encoding='utf-8-sig'))
#         print("Привет")
#         self._set_headers()
#         self.wfile.write(json.dumps(data).encode())
#
#     # POST echoes the message adding a JSON field
#     def do_POST(self):
#         ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
#
#
#         # refuse to receive non-json content
#         if ctype != 'application/json':
#             self.send_response(400)
#             self.end_headers()
#             return
#
#         # read the message and convert it into a python dictionary
#         length = int(self.headers.get('content-length'))
#         message = json.loads(self.rfile.read(length))
#
#         json.dump(message, open('data.json', 'w', encoding='utf-8'))
#         # add a property to the object, just to mess with data
#         message['received'] = 'ok'
#
#         # send the message back
#         self._set_headers()
#         self.wfile.write(json.dumps(message).encode())
#
#
# def run(server_class=HTTPServer, handler_class=Server, port=8080):
#     server_address = ('', port)
#     httpd = server_class(server_address, handler_class)
#
#     print('Starting httpd on port %d...' % port)
#     httpd.serve_forever()
#
#
# if __name__ == "__main__":
#     from sys import argv
#
#     if len(argv) == 2:
#         run(port=int(argv[1]))
#     else:
#         run()


import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


class WSHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def get(self):
        self.write("Hello, world")
        print("ggas")

    def open(self):
        self.clients.append(self)
        print('new connection')
        print(self.clients)
        self.write_message("Hello World")

    def on_message(self, message):
        print('message received %s' % message)

    def on_close(self):
        self.clients.remove(self)
        print('closed connection')


application = tornado.web.Application([
    (r'/ws', WSHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
