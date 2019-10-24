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
