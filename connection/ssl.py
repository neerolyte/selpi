import socket
import ssl
from ssl import SSLSocket

def create_ssl_connection(hostname: str, port: int) -> SSLSocket:
    context = ssl.create_default_context()
    tcp_socket = socket.create_connection((hostname, port))
    return context.wrap_socket(tcp_socket, server_hostname=hostname)
