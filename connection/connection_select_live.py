import settings
from . import Connection
from .ssl import create_ssl_connection

class ConnectionSelectLive(Connection):
    def __init__(
            self,
            create_ssl_connection_function: create_ssl_connection=None,
            username: bytes=None,
            password: bytes=None,
            device: bytes=None

    ):
        super().__init__()
        self.__create_ssl_connection = create_ssl_connection_function or create_ssl_connection
        self.__username = username or settings.getb(b'CONNECTION_SELECT_LIVE_USERNAME')
        self.__password = password or settings.getb(b'CONNECTION_SELECT_LIVE_PASSWORD')
        self.__device = device or settings.getb(b'CONNECTION_SELECT_LIVE_DEVICE')
        self.__socket = None

    def _connect(self):
        hostname = b'select.live'
        port = 7528
        self.__socket = self.__create_ssl_connection(hostname, port)

        # Authenticate
        self._read(1024) # b'LOGIN\r\n'
        self._write(b'USER:'+self.__username+b':'+self.__password+b'\r\n')
        self._read(1024) # b'OK\r\n'

        # Connect
        self._write(b'CONNECT:'+self.__device+b'\r\n')
        self._read(1024) # b'OK\r\n'

    def _read(self, length: int):
        return self.__socket.read(length)

    def _write(self, data: bytes):
        return self.__socket.write(data) # raising ssl.SSLZeroReturnError: TLS/SSL connection has been closed (EOF) (_ssl.c:2472
