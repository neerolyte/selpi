import serial
from config import Config

class Connection:
    def __init__(self):
        self._config = Config()

    def read(self, length: int):
        raise NotImplementedError

    def write(self, data: bytes):
        raise NotImplementedError


class ConnectionSerial(Connection):
    def __init__(self):
        super().__init__()
        self.__port = serial.Serial(
            self._config.get('port'),
            baudrate = self._config.get('baudrate'),
            timeout = 0.01
        )
        self.__port.flushOutput()

    def write(self, data: bytes):
        self.__port.write(data)
        self.__port.flushOutput()

    def read(self, length: int) -> bytes:
        buf = bytearray()
        attempts = length + 2 # Allow for a few timeouts @ 0.5s
        for i in range(1, attempts):
            buf.extend(self.__port.read())
            if len(buf) >= length:
                break
        return buf
