from . import Connection

class ConnectionTCP(Connection):
    def _connect(self):
        hostname = os.getenvb(b'SELPI_CONNECTION_TCP_HOSTNAME')
        port = int(os.getenvb(b'SELPI_CONNECTION_TCP_PORT'))
        self.__sock = socket.create_connection((hostname, port))

    def _read(self, length: int):
        return self.__sock.recv(length)

    def _write(self, data: bytes):
        return self.__sock.send(data)
