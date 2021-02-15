from binascii import Error
from exception import NotFoundException, OutOfBoundsException, ValidationException
from unittest import TestCase
from unittest.mock import Mock
from memory import Range, Data
from unittest_data_provider import data_provider
from exception import NotFoundException, ValidationException

class DataTest(TestCase):
    def test_bytes_raises_before_set(self):
        data = Data(Mock())
        with self.assertRaises(NotFoundException) as context:
            data.bytes
        self.assertEqual(
            'Unable to read bytes before property is set',
            context.exception.args[0]
        )

    @data_provider(lambda: (
        (Range(0xcafe, 1), b'ab'),
        (Range(0xfeed, 5), b'1234567890'),
    ))
    def test_bytes(self, range: Range, bytes: bytes):
        data = Data(range)
        data.bytes = bytes
        self.assertEqual(bytes, data.bytes)

    @data_provider(lambda: (
        (Range(0xcafe, 2), b'ab', 'Unable to store 2 bytes to range requiring 4'),
        (Range(0xfeed, 1), b'1234567890', 'Unable to store 10 bytes to range requiring 2'),
    ))
    def test_bytes_raises_setter(self, range, bytes, expected):
        data = Data(range)
        with self.assertRaises(ValidationException) as context:
            data.bytes = bytes
        self.assertEqual(expected, context.exception.args[0])
