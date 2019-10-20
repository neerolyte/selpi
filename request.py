import struct
from crc import CRC

class Request:
    def __init__(self, address: int, length: int):
        self.__address = address
        self.__length = length

    def message(self) -> bytes:
        msg = bytearray(
            b''.join([
                b'Q',
                struct.pack("<B", self.__length),
                struct.pack("<I", self.__address)
            ])
        )
        msg.extend(CRC(msg).as_bytes())
        return msg

    """
    Get the length of memory requested
    """
    def length(self) -> int:
        return self.__length
