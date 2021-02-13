import unittest, struct
import connection
from connection import ConnectionSelectLive, ConnectionSerial
import os

class ConnectionTest(unittest.TestCase):
    def test_create_serial(self):
        os.environb[b'SELPI_CONNECTION_TYPE'] = b'Serial'
        con = connection.create()
        self.assertIsInstance(con, ConnectionSerial)

    def test_create_select_live(self):
        os.environb[b'SELPI_CONNECTION_TYPE'] = b'SelectLive'
        con = connection.create()
        self.assertIsInstance(con, ConnectionSelectLive)

    def test_create_foo(self):
        os.environb[b'SELPI_CONNECTION_TYPE'] = b'Foo'
        self.assertRaisesRegex(
            NotImplementedError,
            "Connection type not implemented: 'Foo'",
            connection.create
        )

if __name__ == '__main__':
    unittest.main()
