from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from gripcontrol import decode_websocket_events, GripPubControl
import time
from pubcontrol import Item
from gripcontrol import WebSocketMessageFormat

class WebServerHandler(BaseHTTPRequestHandler):
    cname = str("httpnotsupported")

    def do_GET(self):
        self.send_response(200)
        self.send_header('Grip-Hold', 'stream')
        self.send_header('Grip-Channel', self.cname)
        self.end_headers()
        self.wfile.write(b'Channel created')
        print(self.cname)

    def publish_message(self):
        time.sleep(3)
        message = 'Please connect with Websocket. Http-stream is not supported yet!'
        print(message)
        grippub = GripPubControl({'control_uri': 'http://localhost:5561'})
        grippub.publish(self.cname, Item(WebSocketMessageFormat(message)))


server = HTTPServer(('', 8080), WebServerHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
