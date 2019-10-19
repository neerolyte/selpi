import struct
from crc import CRC

class Protocol:
    def get_hello_msg(self) -> bytes:
        return self.get_query_msg(0xa000, 0)

    def get_query_msg(self, address: int, length: int) -> bytes:
        msg = bytearray(
            b''.join([
                b'Q',
                struct.pack("<B", length),
                struct.pack("<H", address),
                b'\0\0'
            ])
        )
        msg.extend(CRC(msg).as_bytes())
        return msg
