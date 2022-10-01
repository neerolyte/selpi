from . import Connection
import settings
import socket
from exception import ConnectionLostException
import logging

class ConnectionTCP(Connection):
    def _connect(self):
        hostname = settings.getb(b'CONNECTION_TCP_HOSTNAME')
        port = int(settings.getb(b'CONNECTION_TCP_PORT'))
        self.__sock = socket.create_connection((hostname, port))

    def _read(self, length: int):
        return self.__sock.recv(length)

    def _write(self, data: bytes):
        attempts = 0
        while attempts < 3:
            try:
                return self.__sock.send(data)
            except BrokenPipeError:
                logging.debug("BrokenPipeError, retrying connection")
                self._connect()
                attempts = attempts + 1
        raise ConnectionLostException("Too many sequential write failures (%s)" % attempts)
