import serial
from config import Config

class Connection:
    def __init__(self):
        self._config = Config()

    def read(self, length: int):
        raise NotImplementedError

    def write(self, data: bytes):
        raise NotImplementedError

#    """
#    Query a block of memory from the SP PRO
#    """
#    def query(self, address: int, length, int) -> bytes:
#        req = Request(address, length)
#        self.write(req.message())
#        res = Response(req)
#        res.set_data(connection.read(res.expected_length()))
#        return res

class ConnectionSerial(Connection):
    def __init__(self):
        super().__init__()
        self.__port = serial.Serial(
            self._config.get('port'),
            baudrate = self._config.get('baudrate'),
            timeout = 0.5
        )
        self.__port.flushOutput()

    def write(self, data: bytes):
        self.__port.write(data)
        self.__port.flushOutput()

    def read(self, length: int) -> bytes:
        buf = bytearray()
        attempts = length + 10 # Allow for a few timeouts @ 0.5s
        for i in range(1, attempts):
            buf.extend(self.__port.read())
            if len(buf) == length:
                break
        return buf
