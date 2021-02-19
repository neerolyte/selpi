from . import Connection
import os
import socket
import ssl

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
        return self.__sock.write(data) # raising ssl.SSLZeroReturnError: TLS/SSL connection has been closed (EOF) (_ssl.c:2472
