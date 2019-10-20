from unittest import TestCase
from response import Response
from request import Request
from error import ValidationError

class TestResponse(TestCase):
    def test_expected_length_0(self):
        req = Request.create_query(0xa000, 0)
        self.assertEqual(12, Response(req).expected_length())

    def test_expected_length_0(self):
        req = Request.create_query(0xa000, 0xff)
        self.assertEqual(12+255*2, Response(req).expected_length())

    def test_valid_no_data(self):
        req = Request.create_query(0xa000, 0) # client hello
        res = Response(req)
        self.assertFalse(res.valid())

    def test_valid_short_data(self):
        req = Request.create_query(0xa000, 0) # client hello
        res = Response(req)
        res_msg = bytearray(req.get_message())
        res_msg.extend(b'\x00\x00')
        res.set_message(res_msg)
        self.assertFalse(res.valid())

    def test_validate_wrong_data(self):
        req = Request.create_query(0xa000, 0) # client hello
        res = Response(req)
        res_msg = bytearray(req.get_message())
        res_msg.extend(b'\x01\x02')
        res_msg.extend(b'\x03\x04')
        res.set_message(res_msg)
        response = b'12345678901234567890123456'
        with self.assertRaises(ValidationError) as context:
            res.validate()
        self.assertEqual(
            'Incorrect CRC (0x4fc5)',
            context.exception.args[0]
        )

