from unittest import TestCase, skip
from unittest.mock import MagicMock, call
from protocol import Protocol
from connection import Connection
from crc import CRC
from exception import ValidationException

from tests.examples import protocol as examples

def mock_connection(data: bytes):
    connection = Connection()
    connection.read = MagicMock(return_value = data)
    connection.write = MagicMock()
    return connection

class ProtocolTest(TestCase):
    def test_query_hello(self):
        example = examples.get('hello')
        connection = mock_connection(example.get('read'))
        protocol = Protocol(connection)
        self.assertEqual(b'\x01\0', protocol.query(0xa000, 0))
        connection.write.assert_called_once_with(example.get('sent'))

    def test_query_auth_init_0(self):
        example = examples.get('auth_init_0')
        connection = mock_connection(example.get('read'))
        protocol = Protocol(connection)
        self.assertEqual(b'z\xb2\x9f\xdeh\x1a\xe0\xb1\'\'\x08\x8f\x80\xc4\xba\x8b', protocol.query(0x1f0000, 7))
        connection.write.assert_called_once_with(example.get('sent'))


    def test_query_short_response(self):
        protocol = Protocol(mock_connection(b'123456'))
        with self.assertRaises(ValidationException) as context:
            protocol.query(0xa000, 8)
        self.assertEqual(
            'Incorrect data length (6 of 28 bytes)',
            context.exception.args[0]
        )

    def test_query_invalid_crc_response(self):
        response = b'12345678901234567890123456'
        protocol = Protocol(mock_connection(response))
        with self.assertRaises(ValidationException) as context:
            protocol.query(0xa000, 7)
        self.assertEqual(
            'Incorrect CRC (0x958a)',
            context.exception.args[0]
        )

    def test_login_auth_0(self):
        init = examples.get('auth_init_0')
        login = examples.get('auth_login_0')
        connection = Connection()
        connection.read = MagicMock(side_effect = [
            init.get('read'),
            login.get('read')
        ])
        connection.write = MagicMock()
        protocol = Protocol(connection)
        protocol.login()
        calls = connection.write.call_args_list
        connection.write.assert_has_calls([
            call(init.get('sent')),
            call(login.get('sent')),
        ])

    @skip("TODO")
    def test_login_failed(self):
        pass

    @skip("TODO")
    def test_login_alternative_password(self):
        pass

