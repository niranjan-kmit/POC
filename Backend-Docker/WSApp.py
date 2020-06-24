import threading
import time
from pubcontrol import Item
from http.server import BaseHTTPRequestHandler, HTTPServer
from gripcontrol import decode_websocket_events, GripPubControl
from gripcontrol import encode_websocket_events, WebSocketEvent
from gripcontrol import websocket_control_message, validate_sig
from gripcontrol import WebSocketMessageFormat
from common import get_channel_name
from common import create_siddhi_common
from common import verify_cookie

from dynamic_siddhi_apps.create_app import create_siddhi_config
import logging
import logging.config
import json
from http.cookies import SimpleCookie

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class GripHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET")
        self.reply_message()


    def do_POST(self):
        print("POST")
        self.reply_message()


    def reply_message(self):

        # Open the WebSocket and subscribe it to a channel:
        request_body = self.rfile.read(int(self.headers.get('Content-Length')))
        cookies = SimpleCookie(self.headers.get('Cookie'))
        token = cookies['SP_SSO_JWT_COOKIE'].value
        if (not verify_cookie(token)):
            self.send_response(401)
            return ;

        # Set the headers required by the GRIP proxy:
        self.send_response(200)
        self.send_header('Sec-WebSocket-Extensions', 'grip; message-prefix=""')
        self.send_header('Content-Type', 'application/websocket-events')
        self.end_headers()
        in_events = decode_websocket_events(request_body)
        if in_events[0].type == 'OPEN':
            out_events = []
            out_events.append(WebSocketEvent('OPEN'))
            self.wfile.write(encode_websocket_events(out_events))
            logger.info("Connection Opened with Client")
            print("Connection Opened with Client")
        if in_events[0].type == 'TEXT':
            print("Text received from client")
            message = in_events[0].content
            print(message)
            cname = get_channel_name(message)
            print(cname)
            if cname != "all":
                try:
                    create_siddhi_common(message, cname)
                except Exception as e:
                    logger.info("Exception occurred:" +  str(e))
                    print("Exception occurred:" +  str(e))
                    threading.Thread(target=self.publish_message(cname, 'Error while creating the Siddhi app')).start()
                else:
                    logger.info("Siddhi app created")
                    print("Siddhi app created")
                    threading.Thread(target=self.publish_message(cname, 'Created Siddhi app: ' + cname)).start()
            else:
                threading.Thread(target=self.publish_message(cname, 'Please publish a valid Json.' )).start()
                print("Invalid JSON")
            out_events = []
            out_events.append(WebSocketEvent('TEXT', 'c:' + websocket_control_message('subscribe', {'channel': cname})))
            self.wfile.write(encode_websocket_events(out_events))
            print("End of the response")

    def publish_message(self, cname, messagetoclient):
        # Wait and then publish a message to the subscribed channel:
        time.sleep(10)
        grippub = GripPubControl({'control_uri': 'http://pushpin-svc:5561'})
        logger.info("Publishing the message " +  messagetoclient)
        print("Publishing the message " + messagetoclient)
        grippub.publish(cname, Item(WebSocketMessageFormat(messagetoclient)))


server = HTTPServer(('', 8090), GripHandler)
try:
    print("Server is waiting to process the request")
#    message = {
#        "type": "heards_sub_req", "conflationDelivery": "first", "conflationType": "C5",
#        "criteria": { "geographies": ["Europe","AUS"], "commodities": ["oil","gas"]},
#        "correlationId": "Test123", "source": "PLATTS"
#    }
#    cname = get_channel_name(json.dumps(message))
#    create_siddhi_common(json.dumps(message), "TestApp")
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
