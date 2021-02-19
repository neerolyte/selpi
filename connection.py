import settings
import serial
import os
import socket
import ssl

def create():
    connectionType = os.getenvb(b'SELPI_CONNECTION_TYPE')
    if connectionType == b'Serial':
        return ConnectionSerial()
    elif connectionType == b'SelectLive':
        return ConnectionSelectLive()
    elif connectionType == b'TCP':
        return ConnectionTCP()
    else:
        raise NotImplementedError("Connection type not implemented: '"+connectionType.decode('ascii')+"'")

class Connection:
    def __init__(self):
        self.__connected = False

    def connect(self):
        if self.__connected:
            return
        self._connect()
        self.__connected = True

    def _connect(self):
        raise NotImplementedError

    def read(self, length: int):
        self.connect()
        return self._read(length)

    def _read(self, length: int):
        raise NotImplementedError

    def write(self, data: bytes):
        self.connect()
        return self._write(data)

    def _write(self, data: bytes):
        raise NotImplementedError

class ConnectionSerial(Connection):
    def _connect(self):
        self.__port = serial.Serial(
            os.getenvb(b'SELPI_CONNECTION_SERIAL_PORT'),
            baudrate = os.getenvb(b'SELPI_CONNECTION_SERIAL_BAUDRATE'),
            timeout = 0.1
        )
        self.__port.flushOutput()

    def _write(self, data: bytes):
        self.__port.write(data)
        self.__port.flushOutput()

    def _read(self, length: int) -> bytes:
        return self.__port.read(length)


class ConnectionSelectLive(Connection):
    def _connect(self):
        hostname = b'select.live'
        port = 7528
        username = os.getenvb(b'SELPI_CONNECTION_SELECT_LIVE_USERNAME')
        password = os.getenvb(b'SELPI_CONNECTION_SELECT_LIVE_PASSWORD')
        device = os.getenvb(b'SELPI_CONNECTION_SELECT_LIVE_DEVICE')
        context = ssl.create_default_context()
        plainSocket = socket.create_connection((hostname, port))
        self.__sock = context.wrap_socket(plainSocket, server_hostname=hostname)

        # Authenticate
        self._read(1024) # b'LOGIN\r\n'
        self._write(b'USER:'+username+b':'+password+b'\r\n')
        self._read(1024) # b'OK\r\n'

        # Connect
        self._write(b'CONNECT:'+device+b'\r\n')
        self._read(1024) # b'OK\r\n'

    def _read(self, length: int):
        return self.__sock.read(length)

    def _write(self, data: bytes):
        return self.__sock.write(data)

class ConnectionTCP(Connection):
    def _connect(self):
        hostname = os.getenvb(b'SELPI_CONNECTION_TCP_HOSTNAME')
        port = int(os.getenvb(b'SELPI_CONNECTION_TCP_PORT'))
        self.__sock = socket.create_connection((hostname, port))

    def _read(self, length: int):
        return self.__sock.recv(length)

    def _write(self, data: bytes):
        return self.__sock.send(data)


