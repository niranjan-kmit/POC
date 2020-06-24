from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from gripcontrol import decode_websocket_events, GripPubControl


class WebServerHandler(BaseHTTPRequestHandler):
    cname = str("httpnotsupported")

    def do_GET(self):
        # cname = self._get_query_param('cname')
        #cname = str(cname)
        # if cname == "None":
        self.send_response(200)
        self.send_header('Grip-Hold', 'stream')
        self.send_header('Grip-Channel', cname)
        self.end_headers()
        self.wfile.write(b'Channel created')
        print(cname)

    # def _get_query_param(self, param_name):
        #    try:
        #   path, _, query_string = self.path.partition('?')
        #   query = parse_qs(query_string)
        #   if param_name in query:
        #       return query[param_name][0]
        #   except Exception as ex:
        #   return str("None")

   def publish_message(self):
        time.sleep(3)
        message = 'Please connect with Websocket. Http-stream is not supported yet!'
        print(message)
        grippub = GripPubControl({'control_uri': 'http://localhost:5561'})
        grippub.publish(cname, Item(WebSocketMessageFormat(message)))


server = HTTPServer(('', 8080), WebServerHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
