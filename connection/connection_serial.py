import serial
from . import Connection
import settings

class ConnectionSerial(Connection):
    def _connect(self):
        self.__port = serial.Serial(
            port = settings.getb(b'CONNECTION_SERIAL_PORT').decode('utf-8'),
            baudrate = settings.getb(b'CONNECTION_SERIAL_BAUDRATE'),
            timeout = 0.1
        )
        self.__port.flushOutput()

    def _write(self, data: bytes):
        self.__port.write(data)
        self.__port.flushOutput()

    def _read(self, length: int) -> bytes:
        return self.__port.read(length)
