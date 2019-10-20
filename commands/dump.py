import struct, hashlib, binascii, config
from crc import CRC
from config import Config
from connection import ConnectionSerial
from protocol import Protocol

def add_parser(subparsers):
    parser = subparsers.add_parser('dump', help='dump memory to stdout')
    parser.set_defaults(func=run)

def run(args):
    connection = ConnectionSerial()
    protocol = Protocol(connection)
    protocol.login()

    # Before 0xa001 we don't get anything back
    start=0xa001
    # How much to get at a time (also tied to console line length currently)
    length=0x10
    # When to stop
    end=0xa2ff
    for address in range(start, end, length):
        hexaddy = binascii.hexlify(struct.pack(">H", address))
        mem = binascii.hexlify(protocol.query(address, length))
        print(b''.join([b'0x',hexaddy,b' ',mem]).decode('utf-8'))
