from exception import ValidationException
import struct
from connection import Connection
from . import Response
from . import Request
from . import Range, Data
import hashlib
import os

class Protocol:
    def __init__(self, connection: Connection, password: bytes=None):
        self.__connection = connection
        self.__password = password or os.getenvb(b'SELPI_SPPRO_PASSWORD')

    """
    Request memory from the SP Pro
    """
    def query(self, range: Range) -> Data:
        req = Request.create_query(range.address, range.words - 1)
        res = self.send(req)
        return res.memory()

    """
    Write some data to memory in the SP Pro
    """
    def write(self, address: int, data: bytes):
        request = Request.create_write(address, data)
        response = self.send(request)
        if not request.get_message() == response.get_message():
            raise Exception("Write check failed, expected '%s' got '%s" % (request.get_message(), response.get_message()))

    def send(self, request: Request) -> Response:
        self.__connection.write(request.get_message())
        res = Response(request)
        message = self.__connection.read(res.expected_length())
        res.set_message(message)
        return res

    def login(self):
        # Get data from SP Pro to combine with password and hash
        data = bytearray(self.query(Range(0x1f0000, 8)))

        # Compute MD5 hash to send back, including login password
        padded_password = self.__password.ljust(32)
        data.extend(padded_password)

        # Compute md5
        md5 = bytearray(hashlib.md5(data).digest())

        # Convert md5 to little endian int32 array
        md5ia = []
        for i in range(0, len(md5), 2):
            md5ia.extend(struct.unpack("<I", bytes(md5[i:i+2] + bytearray([0, 0]))))

        # Convert data from int[] to byte[], little endian but reversing the byte order (thanks Selectronic :( )
        ba = bytearray()
        for x in md5ia:
            bb = bytearray(struct.pack("<I", x)[0:2])
            bb.reverse()
            ba.extend(bb)

        # respond with hash/pwd MD5
        self.write(0x1f0000, ba)

        login_status = struct.unpack('<H', self.query(Range(0x1f0010, 1)))[0]
        if login_status != 1:
            raise ValidationException("Login failed")
