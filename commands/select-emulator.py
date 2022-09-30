from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from statistics import Statistics

statistics = Statistics()

def add_parser(subparsers):
    parser = subparsers.add_parser('select-emulator', help='select.live device emulation')
    parser.set_defaults(func=run)

def run(args):
    server_address = ('', 8000)
    print("Starting server")
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    httpd.serve_forever()

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        return self.do_GET_api()

    def do_GET_api(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        data = json.dumps(
            obj=statistics.get_select_emulated(),
            indent=2,
            separators=(',', ':')
        )
        self.wfile.write(bytes(data, "utf-8"))
        self.wfile.write(b'\n')
