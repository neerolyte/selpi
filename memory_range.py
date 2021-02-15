import struct
import hashlib
import binascii

# Maximum number of words that can retrieved at one time
MAX_WORDS=256

"""
Combine a set of memory ranges in to a list of ranges that can sent
"""
def combine(ranges: list) -> list:
    return _combine(sorted(ranges))

def _combine(ranges: list) -> list:
    if len(ranges) <= 1:
        return ranges
    r1 = ranges[0]
    r2 = ranges[1]
    words = r2.address - r1.address + r2.words
    if words > MAX_WORDS:
        return [r1] + _combine(ranges[1:])
    return _combine([Range(r1.address, words)] + ranges[2:])

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
