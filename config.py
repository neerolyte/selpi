defaults = {
    "port": "/dev/ttyUSB0",
     # Options: 57600 115200 9600 2400 1200 4800 19200 38400
    "baudrate": 57600,
    "password": "Selectronic SP PRO",
}

class Config:
    def get(self, name: str):
        return defaults[name]
