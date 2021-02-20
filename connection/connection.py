class Connection:
    def __init__(self):
        self.__connected = False

    def connect(self):
        if self.__connected:
            return
        self._connect()
        self.__connected = True

    def _connect(self):
        raise NotImplementedError

    def read(self, length: int):
        self.connect()
        return self._read(length)

    def _read(self, length: int):
        raise NotImplementedError

    def write(self, data: bytes):
        self.connect()
        return self._write(data)

    def _write(self, data: bytes):
        raise NotImplementedError


