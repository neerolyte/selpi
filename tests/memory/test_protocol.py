from unittest import TestCase, skip
from unittest.mock import call, create_autospec
from memory import Protocol, Range, Request
from connection import Connection
from exception import ValidationException

class ProtocolTest(TestCase):
    def test_query_hello(self):
        connection = create_autospec(Connection)
        connection.read.return_value = b'\x51\x00\x00\xa0\x00\x00\x9d\x4b\x01\x00\xd8\x19'
        protocol = Protocol(connection)
        self.assertEqual(b'\x01\0', protocol.query(Range(0xa000, 1)))
        connection.write.assert_called_once_with(b'\x51\x00\x00\xa0\x00\x00\x9d\x4b')

    def test_query_hash(self):
        sent = b'Q\x07\x00\x00\x1f\x00\xcfb'
        read = b"Q\x07\x00\x00\x1f\x00\xcfbz\xb2\x9f\xdeh\x1a\xe0\xb1\'\'\x08\x8f\x80\xc4\xba\x8b\xa0@"
        connection = create_autospec(Connection)
        connection.read.return_value = read
        protocol = Protocol(connection)
        self.assertEqual(
            b'z\xb2\x9f\xdeh\x1a\xe0\xb1\'\'\x08\x8f\x80\xc4\xba\x8b',
            protocol.query(Range(0x1f0000, 8))
        )
        connection.write.assert_called_once_with(sent)

    def test_query_short_response(self):
        connection = create_autospec(Connection)
        connection.read.side_effect = [
            b'123456', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'',
        ]
        protocol = Protocol(connection)
        with self.assertRaises(BufferError) as context:
            protocol.query(Range(0xa000, 9))
        self.assertEqual(
            'Expected 28 bytes, but only able to read 6',
            context.exception.args[0]
        )

    def test_query_invalid_crc_response(self):
        response = b'12345678901234567890123456'
        connection = create_autospec(Connection)
        connection.read.return_value = response
        protocol = Protocol(connection)
        with self.assertRaises(ValidationException) as context:
            protocol.query(Range(0xa000, 8))
        self.assertEqual(
            'Incorrect CRC (0x958a)',
            context.exception.args[0]
        )

    def test_login_default_password(self):
        password = b"Selectronic SP PRO"
        login_hash_sent = b'Q\x07\x00\x00\x1f\x00\xcfb'
        login_hash_read = b"Q\x07\x00\x00\x1f\x00\xcfbz\xb2\x9f\xdeh\x1a\xe0\xb1\'\'\x08\x8f\x80\xc4\xba\x8b\xa0@"
        login_challenge = b'W\x07\x00\x00\x1f\x005z\xb6\xd16\x04\x08\x0c\x87\xce\x81\xc1\x82\xc6o\xa5\xfb5w\xaa'
        login_status_sent = b'Q\x00\x10\x00\x1f\x00\xb2\x91'
        login_status_read = b'Q\x00\x10\x00\x1f\x00\xb2\x91\x01\x00\xd8\x19'
        connection = create_autospec(Connection)
        connection.read.side_effect = [
            login_hash_read,
            login_challenge,
            login_status_read,
        ]
        protocol = Protocol(connection, password)
        protocol.login()
        connection.write.assert_has_calls([
            call(login_hash_sent),
            call(login_challenge),
            call(login_status_sent),
        ])

    def test_login_failed(self):
        password = b"Selectronic SP PRO"
        login_hash_sent = b'Q\x07\x00\x00\x1f\x00\xcfb'
        login_hash_read = b"Q\x07\x00\x00\x1f\x00\xcfbz\xb2\x9f\xdeh\x1a\xe0\xb1\'\'\x08\x8f\x80\xc4\xba\x8b\xa0@"
        login_challenge = b'W\x07\x00\x00\x1f\x005z\xb6\xd16\x04\x08\x0c\x87\xce\x81\xc1\x82\xc6o\xa5\xfb5w\xaa'
        login_status_sent = b'Q\x00\x10\x00\x1f\x00\xb2\x91'
        login_status_read = b'Q\x00\x10\x00\x1f\x00\xb2\x91\x00\x00\x00\x00'
        connection = create_autospec(Connection)
        connection.read.side_effect = [
            login_hash_read,
            login_challenge,
            login_status_read,
        ]
        protocol = Protocol(connection, password)
        with self.assertRaises(ValidationException) as context:
            protocol.login()
        self.assertEqual(
            'Login failed',
            context.exception.args[0]
        )
        connection.write.assert_has_calls([
            call(login_hash_sent),
            call(login_challenge),
            call(login_status_sent),
        ])

    def test_login_alternative_password(self):
        password = b"foo"
        login_hash_sent = b'Q\x07\x00\x00\x1f\x00\xcfb'
        login_hash_read = b'Q\x07\x00\x00\x1f\x00\xcfb\xb7\n\xd7\x15\xab\xccl;{\x96\xf3\x98\xf0z\xbf\x12\x02E'
        login_challenge = b'W\x07\x00\x00\x1f\x005z\xa2\xf1\xdf\xfd\xbaA\xa1\xedD\x12\x82\xe7O\x8d\x15_\xc0\x8b'
        login_status_sent = b'Q\x00\x10\x00\x1f\x00\xb2\x91'
        login_status_read = b'Q\x00\x10\x00\x1f\x00\xb2\x91\x01\x00\xd8\x19'
        connection = create_autospec(Connection)
        connection.read.side_effect = [
            login_hash_read,
            login_challenge,
            login_status_read,
        ]
        protocol = Protocol(connection, password)
        protocol.login()
        connection.write.assert_has_calls([
            call(login_hash_sent),
            call(login_challenge),
            call(login_status_sent),
        ])

    def test_read_retry(self):
        connection = create_autospec(Connection)
        connection.read.side_effect = [
            b'\x51', b'\x00\x00', b'\xa0', b'\x00', b'\x00',
            b'\x9d\x4b\x01\x00', b'\xd8', b'\x19',
        ]
        protocol = Protocol(connection)
        self.assertEqual(b'\x01\0', protocol.query(Range(0xa000, 1)))
        connection.read.assert_has_calls([
            call(12), call(11), call(9), call(8),
            call(7), call(6), call(2), call(1),
        ])
        connection.write.assert_called_once_with(b'\x51\x00\x00\xa0\x00\x00\x9d\x4b')


