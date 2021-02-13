# Temporary test proving out that select.live:7528 can establish a direct
# connection to the SP Pro

import socket
import ssl
import os
from request import Request

username = os.environ.get('SELECT_USER').encode('ascii')
password = os.environ.get('SELECT_PASS').encode('ascii')
device = os.environ.get('SELECT_DEVICE').encode('ascii')

hostname = b'select.live'
port = 7528
context = ssl.create_default_context()

with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:

        # Authenticate 
        print(ssock.read(1024)) # Expect b'LOGIN\r\n'
        ssock.write(b'USER:'+username+b':'+password+b'\r\n')
        print(ssock.read(1024)) # Expect b'OK\r\n'

        # LIST DEVICES 
        #ssock.write(b'LIST DEVICES\r\n')
        #print(ssock.read(1024)) # b'DEVICES:1\r\nDEVICE:123456\r\n'

        # Connect
        ssock.write(b'CONNECT:'+device+b'\r\n')
        print(ssock.read(1024)) # Expect b'OK\r\n'

        # Hello
        helloQuery = Request.create_query(0xa000, 0).get_message()
        print(helloQuery)
        ssock.write(helloQuery)
        print(ssock.read(1024)) # b'Q\x00\x00\xa0\x00\x00\x9dK\x01\x00\xd8\x19'

