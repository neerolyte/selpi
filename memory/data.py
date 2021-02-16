
from exception import NotFoundException, ValidationException
from . import Range

"""
Data for a range of memory
"""
class Data():
    def __init__(self, range: Range, bytes: bytes=None):
        self.__range = range
        if bytes != None:
            self.bytes = bytes
        else:
            self.__bytes = None

    @property
    def range(self):
        return self.__range

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
