from unittest import TestCase, skip
from unittest.mock import create_autospec, call
from connection import ConnectionSelectLive, ssl
from ssl import SSLSocket, SSLZeroReturnError
from exception import ValidationException
import settings
import socket

class CreateTest(TestCase):
    def test_connect_success(self):
        create_ssl_connection = create_autospec(ssl.create_ssl_connection)
        ssl_socket = create_autospec(SSLSocket)
        settings_module = create_autospec(settings)
        settings_module.getb.side_effect = (lambda key:
            {
                b'CONNECTION_SELECT_LIVE_USERNAME': b'foo',
                b'CONNECTION_SELECT_LIVE_PASSWORD': b'bar',
                b'CONNECTION_SELECT_LIVE_DEVICE': b'1234567',
            }[key]
        )
        connection = ConnectionSelectLive(
            create_ssl_connection_function=create_ssl_connection,
            settings_module=settings_module
        )
        create_ssl_connection.side_effect = [ssl_socket]
        ssl_socket.read.side_effect = [
            b'LOGIN\r\n',
            b'OK\r\n',
            b'READY\r\n',
        ]

        connection.connect()

        create_ssl_connection.assert_has_calls([
            call(b'select.live', 7528)
        ])
        ssl_socket.write.assert_has_calls([
            call(b'USER:foo:bar\r\n'),
            call(b'CONNECT:1234567\r\n'),
        ])
        ssl_socket.read.assert_has_calls([
            call(1024), call(1024), call(1024)
        ])

    def test_connect_failure_bad_login_line(self):
        create_ssl_connection = create_autospec(ssl.create_ssl_connection)
        ssl_socket = create_autospec(SSLSocket)
        settings_module = create_autospec(settings)
        settings_module.getb.side_effect = (lambda key:
            {
                b'CONNECTION_SELECT_LIVE_USERNAME': b'foo',
                b'CONNECTION_SELECT_LIVE_PASSWORD': b'bar',
            }[key]
        )
        connection = ConnectionSelectLive(
            create_ssl_connection_function=create_ssl_connection,
            settings_module=settings_module
        )
        create_ssl_connection.side_effect = [ssl_socket]
        ssl_socket.read.side_effect = [
            b'WHAT\r\n',
        ]

        with self.assertRaises(ValidationException) as context:
            connection.connect()

        self.assertEqual(
            "Authentication failed, 'LOGIN' prompt was missing, received b'WHAT\\r\\n' instead",
            context.exception.args[0]
        )
        create_ssl_connection.assert_has_calls([
            call(b'select.live', 7528)
        ])
        ssl_socket.write.assert_has_calls([])
        ssl_socket.read.assert_has_calls([call(1024)])

    def test_connect_failure_bad_user_ok(self):
        create_ssl_connection = create_autospec(ssl.create_ssl_connection)
        ssl_socket = create_autospec(SSLSocket)
        settings_module = create_autospec(settings)
        settings_module.getb.side_effect = (lambda key:
            {
                b'CONNECTION_SELECT_LIVE_USERNAME': b'foo',
                b'CONNECTION_SELECT_LIVE_PASSWORD': b'bar',
            }[key]
        )
        connection = ConnectionSelectLive(
            create_ssl_connection_function=create_ssl_connection,
            settings_module=settings_module
        )
        create_ssl_connection.side_effect = [ssl_socket]
        ssl_socket.read.side_effect = [
            b'LOGIN\r\n',
            b'WHAT\r\n'
        ]

        with self.assertRaises(ValidationException) as context:
            connection.connect()

        self.assertEqual(
            "Authentication failed, username or password not accepted, received b'WHAT\\r\\n'",
            context.exception.args[0]
        )
        create_ssl_connection.assert_has_calls([
            call(b'select.live', 7528)
        ])
        ssl_socket.write.assert_has_calls([])
        ssl_socket.read.assert_has_calls([call(1024), call(1024)])

    def test_connect_failure_bad_device_ok(self):
        create_ssl_connection = create_autospec(ssl.create_ssl_connection)
        ssl_socket = create_autospec(SSLSocket)
        settings_module = create_autospec(settings)
        settings_module.getb.side_effect = (lambda key:
            {
                b'CONNECTION_SELECT_LIVE_USERNAME': b'foo',
                b'CONNECTION_SELECT_LIVE_PASSWORD': b'bar',
                b'CONNECTION_SELECT_LIVE_DEVICE': b'1234567',
            }[key]
        )
        connection = ConnectionSelectLive(
            create_ssl_connection_function=create_ssl_connection,
            settings_module=settings_module
        )
        create_ssl_connection.side_effect = [ssl_socket]
        ssl_socket.read.side_effect = [
            b'LOGIN\r\n',
            b'OK\r\n',
            b'WHAT\r\n',
        ]

        with self.assertRaises(ValidationException) as context:
            connection.connect()

        self.assertEqual(
            "Authentication failed, device not accepted, received b'WHAT\\r\\n'",
            context.exception.args[0]
        )
        create_ssl_connection.assert_has_calls([
            call(b'select.live', 7528)
        ])
        ssl_socket.write.assert_has_calls([])
        ssl_socket.read.assert_has_calls([call(1024), call(1024), call(1024)])

    """
    This appears to occur when the ssl socket has been idle for a while
    """
    def test_write_recovers_from_write_failure(self):
        create_ssl_connection = create_autospec(ssl.create_ssl_connection)
        ssl_socket_a = create_autospec(SSLSocket)
        ssl_socket_b = create_autospec(SSLSocket)
        settings_module = create_autospec(settings)
        settings_module.getb.side_effect = (lambda key:
            {
                b'CONNECTION_SELECT_LIVE_USERNAME': b'foo',
                b'CONNECTION_SELECT_LIVE_PASSWORD': b'bar',
                b'CONNECTION_SELECT_LIVE_DEVICE': b'1234567',
            }[key]
        )
        connection = ConnectionSelectLive(
            create_ssl_connection_function=create_ssl_connection,
            settings_module=settings_module
        )
        create_ssl_connection.side_effect = [ssl_socket_a, ssl_socket_b]
        ssl_socket_a.read.side_effect = [
            b'LOGIN\r\n',
            b'OK\r\n',
            b'READY\r\n',
        ]
        ssl_socket_a.write.side_effect = [
            len(b'USER:foo:bar\r\n'),
            len(b'CONNECT:1234567\r\b'),
            SSLZeroReturnError("TLS/SSL connection has been closed (EOF)"),
        ]
        ssl_socket_b.read.side_effect = [
            b'LOGIN\r\n',
            b'OK\r\n',
            b'READY\r\n',
        ]
        ssl_socket_b.write.side_effect = [
            len(b'USER:foo:bar\r\n'),
            len(b'CONNECT:1234567\r\b'),
            len(b'some-data'),
        ]

        connection.connect()
        written = connection.write(b"some-data")

        self.assertEqual(len(b'some-data'), written)
        create_ssl_connection.assert_has_calls([
            call(b'select.live', 7528)
        ])
        ssl_socket_a.write.assert_has_calls([
            call(b'USER:foo:bar\r\n'),
            call(b'CONNECT:1234567\r\n'),
            call(b'some-data'),
        ])
        ssl_socket_b.write.assert_has_calls([
            call(b'USER:foo:bar\r\n'),
            call(b'CONNECT:1234567\r\n'),
        ])
        ssl_socket_a.read.assert_has_calls([
            call(1024), call(1024), call(1024)
        ])
        ssl_socket_b.read.assert_has_calls([
            call(1024), call(1024), call(1024)
        ])

    def test_read_recovers_from_timeout(self):
        create_ssl_connection = create_autospec(ssl.create_ssl_connection)
        ssl_socket_a = create_autospec(SSLSocket)
        ssl_socket_b = create_autospec(SSLSocket)
        settings_module = create_autospec(settings)
        settings_module.getb.side_effect = (lambda key:
            {
                b'CONNECTION_SELECT_LIVE_USERNAME': b'foo',
                b'CONNECTION_SELECT_LIVE_PASSWORD': b'bar',
                b'CONNECTION_SELECT_LIVE_DEVICE': b'1234567',
            }[key]
        )
        connection = ConnectionSelectLive(
            create_ssl_connection_function=create_ssl_connection,
            settings_module=settings_module
        )
        create_ssl_connection.side_effect = [ssl_socket_a, ssl_socket_b]
        ssl_socket_a.read.side_effect = [
            b'LOGIN\r\n',
            b'OK\r\n',
            b'READY\r\n',
            socket.timeout("The read operation timed out"),
        ]
        ssl_socket_a.write.side_effect = [
            len(b'USER:foo:bar\r\n'),
            len(b'CONNECT:1234567\r\b'),
        ]
        ssl_socket_b.read.side_effect = [
            b'LOGIN\r\n',
            b'OK\r\n',
            b'READY\r\n',
            b'some-data',
        ]
        ssl_socket_b.write.side_effect = [
            len(b'USER:foo:bar\r\n'),
            len(b'CONNECT:1234567\r\b'),
        ]

        connection.connect()
        read = connection.read(1024)

        self.assertEqual(b'some-data', read)
        create_ssl_connection.assert_has_calls([
            call(b'select.live', 7528)
        ])
        ssl_socket_a.write.assert_has_calls([
            call(b'USER:foo:bar\r\n'),
            call(b'CONNECT:1234567\r\n'),
        ])
        ssl_socket_b.write.assert_has_calls([
            call(b'USER:foo:bar\r\n'),
            call(b'CONNECT:1234567\r\n'),
        ])
        ssl_socket_a.read.assert_has_calls([
            call(1024), call(1024), call(1024)
        ])
        ssl_socket_b.read.assert_has_calls([
            call(1024), call(1024), call(1024)
        ])
