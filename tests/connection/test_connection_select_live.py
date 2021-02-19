from unittest import TestCase, skip

class CreateTest(TestCase):
    @skip("todo")
    def test_write_when_ssl_socket_closed(self):
        pass

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
