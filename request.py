import struct
from crc import CRC

class Request:
    def __init__(self, address: int):
        self.__address = address

    """
    Get the message as sent over the wire
    """
    def get_message(self) -> bytes:
        msg = bytearray(
            b''.join([
                self.get_type(),
                struct.pack("<B", self.get_length()),
                struct.pack("<I", self.get_address())
            ])
        )
        msg.extend(CRC(msg).as_bytes())
        return msg

    def get_type(self) -> bytes:
        raise NotImplementedError()

    """
    Get the number of words either being requested or written minus 1
    """
    def get_length(self) -> int:
        raise NotImplementedError()

    def get_address(self) -> int:
        return self.__address

class ReadRequest(Request):
    def __init__(self, address: int, length: int):
        super().__init__(address)
        self.__length = length

    def get_type(self) -> bytes:
        return b'Q'

    """
    Get the length of memory requested
    """
    def get_length(self) -> int:
        return self.__length

class WriteRequest(Request):
    def __init__(self, address: int, data: bytes):
        super().__init__(address)
        self.__data = data

    def get_type(self) -> bytes:
        return b'W'

    def get_length(self) -> int:
        return len(self.__data) // 2 - 1

    def get_message(self) -> bytes:
        msg = super().get_message()
        msg.extend(self.__data)
        msg.extend(CRC(msg).as_bytes())
        return msg
