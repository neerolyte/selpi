from unittest import TestCase, skip
from unittest.mock import create_autospec, call
from connection import ConnectionSelectLive, ssl
from ssl import SSLSocket
from exception import ValidationException

class CreateTest(TestCase):
    def test_connect_success(self):
        create_ssl_connection = create_autospec(ssl.create_ssl_connection)
        ssl_socket = create_autospec(SSLSocket)
        username = b'foo'
        password = b'bar'
        device = b'1234567'
        connection = ConnectionSelectLive(
            create_ssl_connection_function=create_ssl_connection,
            username=username,
            password=password,
            device=device
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
        username = b'foo'
        password = b'bar'
        connection = ConnectionSelectLive(
            create_ssl_connection_function=create_ssl_connection,
            username=username,
            password=password
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
        username = b'foo'
        password = b'bar'
        connection = ConnectionSelectLive(
            create_ssl_connection_function=create_ssl_connection,
            username=username,
            password=password
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
        username = b'foo'
        password = b'bar'
        device = b'1234567'
        connection = ConnectionSelectLive(
            create_ssl_connection_function=create_ssl_connection,
            username=username,
            password=password,
            device=device
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

    @skip("todo")
    def test_write_when_ssl_socket_closed(self):
        create_ssl_connection = create_autospec(ssl.create_ssl_connection)
        ssl_socket = create_autospec(SSLSocket)
        connection = ConnectionSelectLive(create_ssl_connection_function=create_ssl_connection)
        create_ssl_connection.side_effect = [ssl_socket]
        ssl_socket.read.side_effect = [
            b'LOGIN\r\n'
        ]

        connection.connect()

        create_ssl_connection.assert_has_calls([
            call(b'select.live', 7528)
        ])

"""
----------------------------------------
Exception happened during processing of request from ('127.0.0.1', 45588)
Traceback (most recent call last):
  File "/usr/lib/python3.8/socketserver.py", line 650, in process_request_thread
    self.finish_request(request, client_address)
  File "/usr/lib/python3.8/socketserver.py", line 360, in finish_request
    self.RequestHandlerClass(request, client_address, self)
  File "/usr/lib/python3.8/socketserver.py", line 720, in __init__
    self.handle()
  File "/usr/lib/python3.8/http/server.py", line 427, in handle
    self.handle_one_request()
  File "/usr/lib/python3.8/http/server.py", line 415, in handle_one_request
    method()
  File ".../selpi/commands/http.py", line 54, in do_GET
    muster.update(variables)
  File ".../selpi/muster.py", line 24, in update
    res = self.__protocol.query(range)
  File ".../selpi/memory/protocol.py", line 21, in query
    res = self.__send(req)
  File ".../selpi/memory/protocol.py", line 34, in __send
    self.__connection.write(request.get_message())
  File ".../selpi/connection.py", line 40, in write
    return self._write(data)
  File ".../selpi/connection.py", line 86, in _write
    return self.__sock.write(data)
  File "/usr/lib/python3.8/ssl.py", line 1118, in write
    return self._sslobj.write(data)
ssl.SSLZeroReturnError: TLS/SSL connection has been closed (EOF) (_ssl.c:2472)
----------------------------------------
"""
