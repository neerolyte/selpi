import unittest
import connection
from connection import ConnectionSelectLive, ConnectionSerial
import os

class CreateTest(unittest.TestCase):
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
  File "/home/dschoen/code/selpi/commands/http.py", line 54, in do_GET
    muster.update(variables)
  File "/home/dschoen/code/selpi/muster.py", line 24, in update
    res = self.__protocol.query(range)
  File "/home/dschoen/code/selpi/memory/protocol.py", line 21, in query
    res = self.__send(req)
  File "/home/dschoen/code/selpi/memory/protocol.py", line 34, in __send
    self.__connection.write(request.get_message())
  File "/home/dschoen/code/selpi/connection.py", line 40, in write
    return self._write(data)
  File "/home/dschoen/code/selpi/connection.py", line 86, in _write
    return self.__sock.write(data)
  File "/usr/lib/python3.8/ssl.py", line 1118, in write
    return self._sslobj.write(data)
ssl.SSLZeroReturnError: TLS/SSL connection has been closed (EOF) (_ssl.c:2472)
----------------------------------------
"""
