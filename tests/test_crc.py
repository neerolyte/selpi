import unittest
from memory import CRC

class CRCTest(unittest.TestCase):
    def test_as_int(self):
        self.assertEqual(CRC(b'Q\x0a\x12\xa0\x00\x00').as_int(), 0xfde2)

    def test_as_hex(self):
        self.assertEqual(CRC(b'Q\x0a\x12\xa0\x00\x00').as_hex(), b'e2fd')
        self.assertEqual(CRC(b'Q\x01\xff\xaf\x00\x00').as_hex(), b'cccf')
