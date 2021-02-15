from unittest import TestCase
from memory import Range, extract
from unittest_data_provider import data_provider
from exception import *

class ExtractTest(TestCase):
    @data_provider(lambda: (
        (Range(0x0000, 10), Range(0x0001, 2), b'1234567890abcdefghij', b'3456'),
    ))
    def test_extract(self, haystack, needle, bytes, expected):
        self.assertEqual(expected, extract(haystack, needle, bytes))

    @data_provider(lambda: (
        (Range(0x0000, 10), Range(0x00010, 2), b'1234567890abcdefghij', b'3456'),
    ))
    def test_extract_out_of_range(self, haystack, needle, bytes, expected):
        with self.assertRaises(OutOfBoundsException) as context:
            extract(haystack, needle, bytes)
        self.assertEqual(
            '%s is outside of %s' % (needle, haystack),
            context.exception.args[0]
        )
        # TODO: what happens if the needle is not in the haystack?
