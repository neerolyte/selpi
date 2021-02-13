import settings
import serial
import os
import socket
import ssl

class Connection:
    def read(self, length: int):
        raise NotImplementedError

    def write(self, data: bytes):
        raise NotImplementedError


class ConnectionSerial(Connection):
    def __init__(self):
        super().__init__()
        self.__port = serial.Serial(
            os.getenvb(b'SELPI_CONNECTION_SERIAL_PORT'),
            baudrate = os.getenvb(b'SELPI_CONNECTION_SERIAL_BAUDRATE'),
            timeout = 0.1
        )
        self.__port.flushOutput()
        self.__buf = bytearray()

    def write(self, data: bytes):
        self.__port.write(data)
        self.__port.flushOutput()

    def read(self, length: int) -> bytes:
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
    def __init__(self):
        super().__init__()
        hostname = b'select.live'
        port = 7528
        username = os.getenvb(b'SELPI_CONNECTION_SELECT_LIVE_USERNAME')
        password = os.getenvb(b'SELPI_CONNECTION_SELECT_LIVE_PASSWORD')
        device = os.getenvb(b'SELPI_CONNECTION_SELECT_LIVE_DEVICE')
        context = ssl.create_default_context()
        plainSocket = socket.create_connection((hostname, port))
        self.__sock = context.wrap_socket(plainSocket, server_hostname=hostname)

        # Authenticate 
        self.read(1024) # b'LOGIN\r\n'
        self.write(b'USER:'+username+b':'+password+b'\r\n')
        self.read(1024) # b'OK\r\n'

        # Connect
        self.write(b'CONNECT:'+device+b'\r\n')
        self.read(1024) # b'OK\r\n'
                
    def read(self, length: int):
        return self.__sock.read(length)

    def write(self, data: bytes):
        return self.__sock.write(data)


