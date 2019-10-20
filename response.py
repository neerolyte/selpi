import struct
from crc import CRC
from request import Request
from error import ValidationError

class Response:
    def __init__(self, request: Request):
        self.__request = request
        self.__data = bytes()

    def expected_length(self) -> int:
        return sum([
            len(self.__request.message()),     # request message
            (self.__request.length() + 1) * 2, # memory requested
            2,                                 # crc
        ])

    def valid(self) -> bool:
        try:
            self.validate()
        except ValidationError:
            return False
        return True

    def validate(self):
        self.validate_length()
        self.validate_crc()

    def validate_length(self):
        actual = len(self.__data)
        expected = self.expected_length()
        if actual == expected:
            return
        raise ValidationError(
            "Incorrect data length (%(actual)i of %(expected)i bytes)"
            % {'actual': actual, 'expected': expected}
        )

    def validate_crc(self):
        crc = CRC(self.__data)
        if crc.as_int() == 0:
            return
        raise ValidationError(
            "Incorrect CRC (0x%(crc)s)" \
            % { 'crc': crc.as_hex().decode("utf-8") }
        )

    def set_data(self, data: bytes):
        self.__data = data

    """
    Get the memory that the SP PRO returned
    TODO: does this make sense for write requests?
    """
    def memory(self) -> bytes:
        self.validate()
        query_length = len(self.__request.message())
        memory_length = (self.__request.length() + 1) * 2
        start = query_length
        end = start + memory_length
        return self.__data[start:end]

