
import struct
import binascii

class Range():
    def __init__(self, address: int, words: int):
        self.__address = address
        self.__words = words

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
