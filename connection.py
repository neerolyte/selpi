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
        self.__buf = bytearray()

    def _write(self, data: bytes):
        self.__port.write(data)
        self.__port.flushOutput()

    def _read(self, length: int) -> bytes:
        attempts = 3
        while len(self.__buf) < length:
            remaining = length - len(self.__buf)
            read = self.__port.read(remaining)
            self.__buf.extend(read)
            # if we don't receive anything a few times in a row, fail
            if len(read) == 0:
                attempts = attempts -1
            if attempts <= 0:
                raise BufferError()
        buf = self.__buf[0:length]
        self.__buf = self.__buf[length:]
        return buf


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


