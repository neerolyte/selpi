from unittest import TestCase
from memory import Range, extract, Data
from unittest_data_provider import data_provider
from exception import *

class ExtractTest(TestCase):
    @data_provider(lambda: (
        (
            Range(0x0001, 2),
            [Data(Range(0x0000, 10), b'1234567890abcdefghij'),],
            Data(Range(0x0001, 2), b'3456'),
        ),
        (
            Range(0x0001, 2),
            [Data(Range(0x0001, 4), b'12345678'),],
            Data(Range(0x0001, 2), b'1234'),
        ),
        (
            Range(0x1234, 4),
            [
                Data(Range(0x0000, 10), b'aaaaaaaaaaaaaaaaaaaa'),
                Data(Range(0x1230, 10), b'mmmmmmmm78901234mmmm'),
                Data(Range(0x9999, 10), b'zzzzzzzzzzzzzzzzzzzz'),
            ],
            Data(Range(0x1234, 4), b'78901234')
        ),
    ))
    def test_extract(self, range, datas, expected):
        self.assertEqual(expected, extract(range, datas))

    @data_provider(lambda: (
        (Range(0x0000, 10), [Data(Range(0x00010, 10),b'1234567890abcdefghij')]),
        (Range(0x0010, 12), [Data(Range(0x00010, 10),b'1234567890abcdefghij')]),
        (Range(0x0011, 5), [Data(Range(0x00010, 5),b'1234567890')]),
        (Range(0xcafe, 1), [Data(Range(0x00010, 5),b'1234567890')]),
    ))
    def test_extract_out_of_range(self, range, datas):
        with self.assertRaises(NotFoundException) as context:
            extract(range, datas)
        self.assertEqual(
            '%s was not found' % range,
            context.exception.args[0]
        )
