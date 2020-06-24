import threading
import time
from pubcontrol import Item
from http.server import BaseHTTPRequestHandler, HTTPServer
from gripcontrol import decode_websocket_events, GripPubControl
from gripcontrol import encode_websocket_events, WebSocketEvent
from gripcontrol import websocket_control_message, validate_sig
from gripcontrol import WebSocketMessageFormat


class GripHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET")
        self.reply_message()

    def do_POST(self):
        print("POST")
        self.reply_message()

    def reply_message(self):
        # Set the headers required by the GRIP proxy:
        self.send_response(200)
        self.send_header('Sec-WebSocket-Extensions', 'grip; message-prefix=""')
        self.send_header('Content-Type', 'application/websocket-events')
        self.end_headers()

        # Open the WebSocket and subscribe it to a channel:
        request_body = self.rfile.read(int(self.headers.get('Content-Length')))
        in_events = decode_websocket_events(request_body)
        if in_events[0].type == 'OPEN':
            out_events = []
            out_events.append(WebSocketEvent('OPEN'))
            self.wfile.write(encode_websocket_events(out_events))
            print("Connection Opened with Client")
        if in_events[0].type == 'TEXT':
            out_events = []
            out_events.append(WebSocketEvent('TEXT', 'c:' + websocket_control_message('subscribe', {'channel': 'all'})))
            self.wfile.write(encode_websocket_events(out_events))
            print("Text received from client")
            threading.Thread(target=self.publish_message).start()

    def publish_message(self):
        # Wait and then publish a message to the subscribed channel:
        time.sleep(3)
        grippub = GripPubControl({'control_uri': 'http://localhost:5561'})
        grippub.publish('all', Item(WebSocketMessageFormat('Channel all created!!')))


server = HTTPServer(('', 8090), GripHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
