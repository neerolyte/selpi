import struct
from crc import CRC

class Request:
    def __init__(self, message: bytes):
        self.__message = message

    def __calculate_message(type: bytes, address: int, length: int) -> bytes:
        msg = bytearray(
            b''.join([
                type,
                struct.pack("<B", length),
                struct.pack("<I", address)
            ])
        )
        msg.extend(CRC(msg).as_bytes())
        return msg

    def calculate_message_length(msg: bytes) -> int:
        if len(msg) < 2:
            raise TypeError("Need at least two bytes")
        type_ = chr(msg[0])
        length = msg[1]
        if type_ == 'Q':
            return 6 + (length + 1) * 2
        raise TypeError("Unknown message type %s" % type_)

    """
    Create a query request.
    Query requests ask for a block of memory from the SP PRO
    """
    def create_query(address: int, length: int):
        msg = Request.__calculate_message(b'Q', address, length)
        return Request(msg)

    def create_write(address: int, data: bytes):
        length = len(data) // 2 - 1
        msg = Request.__calculate_message(b'W', address, length)
        msg.extend(data)
        msg.extend(CRC(msg).as_bytes())
        return Request(msg)

    def create_from_socket(socket):
        return Request(socket.recv(1024))

    def get_message(self) -> bytes:
        return self.__message

    def get_type(self) -> bytes:
        return self.__message[0]

    """
    Get the number of words either being requested or written
    """
    def get_word_length(self) -> int:
        return self.__message[1] + 1

    def get_address(self) -> int:
        return self.__address
