from connection import ConnectionSerial
from protocol import Protocol
import struct
import socket
from config import Config
from request import Request

def add_parser(subparsers):
    parser = subparsers.add_parser('proxy', help='expose SP PRO over TCP proxy')
    parser.set_defaults(func=run)

connection = ConnectionSerial()
protocol = Protocol(connection)

def run(args):
    config = Config()
    address = config.get('proxy_bind_address')
    port = config.get('proxy_bind_port')
    Proxy().bind(address, port)

class Proxy:
    def __init__(self):
        self.__buffer = bytearray()
        self.__serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind(self, address, port):
        self.__serversocket.bind((address, port))
        # become a server socket
        self.__serversocket.listen(5)

        while True:
            print("Waiting for TCP connection on %s:%d" % (address, port))
            self.wait_connection()


    def wait_connection(self):
        (clientsocket, address) = self.__serversocket.accept()
        self.handle_connection(clientsocket)

    def handle_connection(self, socket):
        print("Got connection")
        while True:
            self.wait_message(socket)

    def wait_message(self, socket):
        while (len(self.__buffer) < 2):
            self.__buffer.extend(socket.recv(1))
        print("calculating message length on", self.__buffer)
        wl = Request.calculate_message_length(self.__buffer)
        while len(self.__buffer) < wl:
            self.__buffer.extend(socket.recv(1))
        print("buf before", self.__buffer)
        print("shortening to %d" % wl)
        msg = self.__buffer[0:wl]
        self.__buffer = self.__buffer[wl:]
        print("msg now %d bytes: %s" % (len(msg), msg))
        print("left over buffer", self.__buffer)
        req = Request(msg)
        print("DEBUG: request:  %s" % msg)
        res = protocol.send(req)
        msg = res.get_message()
        print("DEBUG: response: %s" % msg)
        socket.sendall(msg)
