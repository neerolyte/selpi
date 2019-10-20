import struct
from crc import CRC
from connection import Connection
from request import Request
from response import Response

class Protocol:
    def __init__(self, connection: Connection):
        self.__connection = connection

    """
    Request memory from the SP Pro
    """
    def query(self, address: int, length: int) -> bytes:
        req = Request(address, length)
        self.__connection.write(req.message())
        res = Response(req)
        data = self.__connection.read(res.expected_length())
        res.set_data(data)
        return res.memory()

