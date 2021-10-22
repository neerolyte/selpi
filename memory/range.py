
import struct
import binascii

from exception import NotFoundException

"""
A range of memory
"""
class Range():
    def __init__(self, address: int, words: int, bytes: bytes=None):
        self.__address = address
        self.__words = words

    def __init__(self, range: Range, bytes: bytes=None):
        self.__range = range
        self.__bytes = None
        if bytes != None:
            self.bytes = bytes

    def __eq__(self, other):
        return (
            isinstance(other, Range)
            and self.__address == other.__address
            and self.__words == other.__words
        )

    def __lt__(self, other):
        return (
            isinstance(other, Range)
            and self.__address < other.__address
        )

    def __repr__(self):
        hexaddy = '0x'+binascii.hexlify(struct.pack(">H", self.__address)).decode('ascii')
        return 'Range(%s, %s)' % (hexaddy, self.__words)

    @property
    def address(self):
        return self.__address

    @property
    def words(self):
        return self.__words

    @property
    def bytes(self):
        if not self.__bytes:
            raise NotFoundException('Unable to read bytes before property is set')
        return self.__bytes

    @bytes.setter
    def bytes(self, bytes: bytes):
        if len(bytes) == self.range.words * 2:
            self.__bytes = bytes
            return
        raise ValidationException(
            'Unable to store %s bytes to range requiring %s' % (
                len(bytes), self.range.words * 2
            )
        )

    def __lt__(self, other):
        return (
            isinstance(other, Data)
            and self.__range < other.__range
        )

    def __repr__(self):
        return 'Data(%s, %s)' % (self.__range, self.__bytes)

    def __eq__(self, other):
        return (
            isinstance(other, Data)
            and self.__range == other.__range
            and self.__bytes == other.__bytes
        )
