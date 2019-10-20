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
    #if not res.valid():
    #    print("Invalid response")
    #    return
    print("SP hello received")


    return
    connection = ConnectionSerial()
    req = Request(0xa000, 0)
    print("Sending client hello")
    connection.write(req.message())
    res = Response(req)
    res.set_data(connection.read(res.expected_length()))
    if not res.valid():
        print("Invalid response")
        return
    print("SP hello received")
    #protocol = Protocol()
    #req = protocol.get_hello_msg()
    #print("requesting", req)
    #connection.write(req)
    #length = sum([
    #    # Query components
    #    1, # type
    #    1, # length
    #    2, # address
    #    2, # unknown
    #    2, # crc
    #    # Response components
    #    2, # unknown
    #    2, # crc
    #])
    #res = connection.read(length)
    #print("response", res)
