from unittest import TestCase
from request import ReadRequest
from response import Response

class TestRequest(TestCase):
    def test_as_bytes_hello(self):
        req = ReadRequest(0xa000, 0)
        expected = b'\x51\x00\x00\xa0\x00\x00\x9d\x4b'
        self.assertEqual(expected, req.get_message())

    def test_as_bytes_load_power(self):
        req = ReadRequest(0xa093, 3)
        expected = b'\x51\x03\x93\xa0\x00\x00\x53\x9d'
        self.assertEqual(expected, req.get_message())

    def test_length_0(self):
        self.assertEqual(0, ReadRequest(0xa000, 0).get_length())

    def test_length_ff(self):
        self.assertEqual(255, ReadRequest(0xa000, 0xff).get_length())
