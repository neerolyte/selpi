import connection
from protocol import Protocol
import struct
import memory
import binascii
import logging

class Data:
    def __init__(self):
        self.__protocol = Protocol(connection.create())
        self.__protocol.login()
        self.__scales = None

    def get_scaled(self, name):
        mem_info = memory.MAP[name]
        words = memory.TYPES[mem_info[memory.TYPE]][memory.WORDS]
        rawBytes = self.__protocol.query(mem_info[memory.ADDRESS], words - 1)
        logging.debug("response: 0x%s" % binascii.hexlify(rawBytes).decode('ascii'))
        self.__populate_scales()
        return memory.convert(name, rawBytes, self.__scales)

    def __query(self, name):
        address, dataType, unit = map[name]
        format = types[dataType]["format"]
        words = types[dataType]["words"]
        rawBytes = self.__protocol.query(address, words - 1)
        unscaled = _unpack(format, rawBytes)
        scaleMethod = getattr(self, '_scaleFor'+unit)
        return scaleMethod(unscaled)

    def __populate_scales(self):
        if self.__scales != None:
            return
        mem_info = memory.MAP["CommonScaleForAcVolts"]
        address = mem_info[memory.ADDRESS]
        type = mem_info[memory.TYPE]
        format = memory.TYPES[type][memory.FORMAT]
        scale_mem = self.__protocol.query(address, 5)
        self.__scales = {
            'CommonScaleForAcVolts': struct.unpack(format, scale_mem[0:2])[0],
            'CommonScaleForAcCurrent': struct.unpack(format, scale_mem[2:4])[0],
            'CommonScaleForDcVolts': struct.unpack(format, scale_mem[4:6])[0],
            'CommonScaleForDcCurrent': struct.unpack(format, scale_mem[6:8])[0],
            'CommonScaleForTemperature': struct.unpack(format, scale_mem[8:10])[0],
            'CommonScaleForInternalVoltages': struct.unpack(format, scale_mem[10:12])[0],
        }
