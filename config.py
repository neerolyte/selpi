import os

defaults = {
    "port": "/dev/ttyUSB0",
     # Options: 57600 115200 9600 2400 1200 4800 19200 38400
    "baudrate": 57600,
    "password": "Selectronic SP PRO",
    "proxy_bind_address": '127.0.0.1',
    'proxy_bind_port': 1234,
}

class Config:
    def get(self, name: str):
        return os.getenv(name, defaults[name])
