from unittest import TestCase
from unittest.mock import MagicMock
import request
from request import Request
from response import Response
from tests.examples import protocol as examples

class TestRequest(TestCase):
    def test_as_bytes_hello(self):
        req = Request.create_query(0xa000, 0)
        expected = examples.get('hello').get('sent')
        self.assertEqual(expected, req.get_message())

    def test_as_bytes_load_power(self):
        req = Request.create_query(0xa093, 3)
        expected = b'\x51\x03\x93\xa0\x00\x00\x53\x9d'
        self.assertEqual(expected, req.get_message())

    def test_create_write_auth_login_0(self):
        req = Request.create_write(0x1f0000, b'\xb6\xd16\x04\x08\x0c\x87\xce\x81\xc1\x82\xc6o\xa5\xfb5')
        self.assertEqual(examples.get('auth_login_0').get('sent'), req.get_message())

    def test_word_length_0(self):
        self.assertEqual(1, Request.create_query(0xa000, 0).get_word_length())

    def test_word_length_0(self):
        self.assertEqual(16, Request.create_query(0xa000, 15).get_word_length())

    def test_word_length_ff(self):
        self.assertEqual(256, Request.create_query(0xa000, 0xff).get_word_length())

    def test_calculate_message_length(self):
        self.assertEqual(8, Request.calculate_message_length(b'Q\x00'))
        self.assertEqual(8, Request.calculate_message_length(b'Q\x0f'))
        self.assertEqual(8, Request.calculate_message_length(b'Q\xff'))

    def test_str_hello(self):
        msg = b'\x51\x00\x00\xa0\x00\x00\x9d\x4b'
        request = Request(msg)
        self.assertEqual('Query(0x0000a000)', str(request))

    def test_str_hello(self):
        msg = b'\x51\x00\x00\xa0\x00\x00\x9d\x4b'
        request = Request(msg)
        self.assertEqual('Query(0xa000)', str(request))

    def test_str_abcd_4(self):
        msg = b'\x51\x03\xcd\xab\x00\x00'
        request = Request(msg)
        self.assertEqual('Query(0xabcd-abd1)', str(request))
