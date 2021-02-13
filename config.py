import os

defaults = {
    "proxy_bind_address": '127.0.0.1',
    'proxy_bind_port': 1234,
}

class Config:
    def get(self, name: str):
        return os.getenv(name, defaults[name])
