from . import ConnectionSerial, ConnectionSelectLive, ConnectionTCP
import os

def create():
    connectionType = os.getenvb(b'SELPI_CONNECTION_TYPE')
    if connectionType == b'Serial':
        return ConnectionSerial()
    elif connectionType == b'SelectLive':
        return ConnectionSelectLive()
    elif connectionType == b'TCP':
        return ConnectionTCP()
    else:
        raise NotImplementedError("Connection type not implemented: '"+connectionType.decode('ascii')+"'")
