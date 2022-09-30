import struct,  binascii
from memory import Protocol, Range

def add_parser(subparsers):
    parser = subparsers.add_parser('dump', help='dump memory to stdout')
    parser.set_defaults(func=run)

def run(args):
    protocol = Protocol()

    # Before 0xa001 we don't get anything back
    start=0xa001
    # How much to get at a time
    fetch_words=0x100
    line_words=0x10
    # When to stop
    end=0xa301
    print('          1   2   3   4   5   6   7   8   9   a   b   c   d   e   f   0')
    for address in range(start, end, fetch_words):
        memory = protocol.query(Range(address, fetch_words))
        for offset in range(0, fetch_words, line_words):
            start_bytes = offset * 2
            end_bytes = (offset + line_words) * 2
            sub_memory = memory[start_bytes:end_bytes]
            hex_memory = binascii.hexlify(sub_memory)
            hex_address = binascii.hexlify(struct.pack(">H", address + offset))
            print(b''.join([b'0x',hex_address,b' ',hex_memory]).decode('utf-8'))
