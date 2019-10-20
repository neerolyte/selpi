import struct
from crc import CRC
from connection import Connection
from response import Response
from request import *
import hashlib

class Protocol:
    def __init__(self, connection: Connection):
        self.__connection = connection

    """
    Request memory from the SP Pro
    """
    def query(self, address: int, length: int) -> bytes:
        req = ReadRequest(address, length)
        res = self.send(req)
        return res.memory()

    """
    Write some data to memory in the SP Pro
    """
    def write(self, address: int, data: bytes):
        request = WriteRequest(address, data)
        response = self.send(request)
        if not request.get_message() == response.get_message():
            raise Exception("todo: write check failed?")

    def send(self, request: Request) -> Response:
        self.__connection.write(request.get_message())
        res = Response(request)
        message = self.__connection.read(res.expected_length())
        res.set_message(message)
        return res

    def login(self):
        # Get data from SP Pro to combine with password and hash
        data = bytearray(self.query(0x1f0000, 7))

        # Compute MD5 hash to send back, including login password
        data.extend("Selectronic SP PRO".ljust(32).encode("ascii"))

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
