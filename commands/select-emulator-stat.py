from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from statistics import Statistics

statistics = Statistics()

def add_parser(subparsers):
    parser = subparsers.add_parser('select-emulator-stat', help='select.live device emulation')
    parser.set_defaults(func=run)

def run(args):
	print(json.dumps(
		obj=statistics.get_select_emulated(),
		indent=2,
		separators=(',', ':')
	))
