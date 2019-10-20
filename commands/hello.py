from connection import ConnectionSerial
from protocol import Protocol
from request import Request
from response import Response

def add_parser(subparsers):
    parser = subparsers.add_parser('hello', help='send a hello')
    parser.set_defaults(func=run)

def run(args):
    connection = ConnectionSerial()
    protocol = Protocol(connection)
    print("Sending client hello")
    protocol.query(0xa000, 0)
    print("SP hello received")
