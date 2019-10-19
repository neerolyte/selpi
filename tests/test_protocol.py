import unittest, struct
from protocol import Protocol

class ProtocolTest(unittest.TestCase):
    """
    SP LINK sends 4x of these when checking that it's talking to a SP Pro.
    Simplest way to check is to listen with `nc -l $port` and then configure SP LINK to do a TCP connection to it.
    """
    def test_calculate_hello_message(self):
        # The format of the message appears to be:
        #   Q (1B) for query (\x51 is a literal Q)
        #   Len (1B) requesting the number of 2 bytes words to return
        #   Address (2BLE) The address to start returning memory from
        #   Null (2B) Reserved?
        #   CRC (2B) Cyclic Reduncancy Check
        #            Q   Len.Address Null    CRC
        expected = b'\x51\x00\x00\xa0\x00\x00\x9d\x4b'
        self.assertEqual(expected, Protocol().get_hello_msg())

if __name__ == '__main__':
    unittest.main() 
