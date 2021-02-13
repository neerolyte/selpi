import struct, hashlib, binascii
from crc import CRC
import connection
from protocol import Protocol

def add_parser(subparsers):
    parser = subparsers.add_parser('dump', help='dump memory to stdout')
    parser.set_defaults(func=run)

def run(args):
    protocol = Protocol(connection.create())
    protocol.login()

    # Before 0xa001 we don't get anything back
    start=0xa001
    # How much to get at a time (also tied to console line length currently)
    length=0x10
    # When to stop
    end=0xa2ff
    print('          1   2   3   4   5   6   7   8   9   a   b   c   d   e   f   0')
    for address in range(start, end, length):
        hexaddy = binascii.hexlify(struct.pack(">H", address))
        mem = binascii.hexlify(protocol.query(address, length - 1))
        print(b''.join([b'0x',hexaddy,b' ',mem]).decode('utf-8'))
