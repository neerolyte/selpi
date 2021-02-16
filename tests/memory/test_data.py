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

    def test_bytes_raises_during_init(self):
        with self.assertRaises(ValidationException) as context:
            Data(Range(0x0000, 1), b'1234')
        self.assertEqual(
            'Unable to store 4 bytes to range requiring 2',
            context.exception.args[0]
        )

    @data_provider(lambda: (
        (Range(0xcafe, 1), b'ab'),
        (Range(0xfeed, 5), b'1234567890'),
    ))
    def test_bytes_getter(self, range: Range, bytes: bytes):
        data = Data(range, bytes)
        self.assertEqual(bytes, data.bytes)

    @data_provider(lambda: (
        (Range(0xcafe, 1), b'ab'),
        (Range(0xfeed, 5), b'1234567890'),
    ))
    def test_bytes_setter(self, range: Range, bytes: bytes):
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

    def test_sorted(self):
        datas = [
            Data(Range(0x1234, 1), b'zz'),
            Data(Range(0x9999, 2), b'aaaa'),
            Data(Range(0x0000, 1), b'mm'),
            Data(Range(0x4567, 1), b'aa'),
        ]
        self.maxDiff = None
        self.assertEqual([
            Data(Range(0x0000, 1), b'mm'),
            Data(Range(0x1234, 1), b'zz'),
            Data(Range(0x4567, 1), b'aa'),
            Data(Range(0x9999, 2), b'aaaa'),
        ], sorted(datas))
