import connection
from protocol import Protocol
import struct

types = {
    "ushort": {
        "format": "<H",
        "words": 1,
    },
    "uint": {
        "format": "<I",
        "words": 2,
    },
}

map = {
    # "Name": [address, type],
    "CommonScaleForAcVolts": [41000, "ushort"],
    "CommonScaleForAcCurrent": [41001, "ushort"],
    "CommonScaleForDcVolts": [41002, "ushort"],
    "CommonScaleForDcCurrent": [41003, "ushort"],
    "CommonScaleForTemperature": [41004, "ushort"],
    "CommonScaleForInternalVoltages": [41005, "ushort"],
    "TotalKacokWhTotalAcc": [41519, "uint"],
    "CombinedKacoAcPowerHiRes": [41896, "uint"],
    "LoadAcPower": [41107, "uint"],
    "ACLoadkWhTotalAcc": [41438, "uint"],
    "BatteryVolts": [41052, "ushort"],
    "DCBatteryPower": [41007, "uint"],
}

class Data:
    def __init__(self):
        self.__protocol = Protocol(connection.create())
        self.__protocol.login()
        self.__commonScaleForAcVolts = None
        self.__commonScaleForAcCurrent = None
        self.__commonScaleForDcVolts = None
        self.__commonScaleForDcCurrent = None
        self.__commonScaleForTemperature = None
        self.__commonScaleForInternalVoltages = None

    def getCommonScaleForAcVolts(self):
        if self.__commonScaleForAcVolts == None:
            self.__populateCommonScales()
        return self.__commonScaleForAcVolts

    def getCommonScaleForAcCurrent(self):
        if self.__commonScaleForAcCurrent == None:
            self.__populateCommonScales()
        return self.__commonScaleForAcCurrent

    def getCommonScaleForDcVolts(self):
        if self.__commonScaleForDcVolts == None:
            self.__populateCommonScales()
        return self.__commonScaleForDcVolts

    def getCommonScaleForDcCurrent(self):
        if self.__commonScaleForDcCurrent == None:
            self.__populateCommonScales()
        return self.__commonScaleForDcCurrent

    def __scaleForAcPower(self, unscaledPower):
        return unscaledPower * self.getCommonScaleForAcVolts() * self.getCommonScaleForAcCurrent() / 26214400.0

    def __scaleForAcEnergy(self, unscaledEnergy):
        return unscaledEnergy * 24 * self.getCommonScaleForAcVolts() * self.getCommonScaleForAcCurrent() / 3276800.0

    def __scaleForDcVolts(self, unscaledVolts):
        return unscaledVolts * self.getCommonScaleForDcVolts() / 327680.0

    def __scaleForDcPower(self, unscaledPower):
        return unscaledPower * self.getCommonScaleForDcVolts() * self.getCommonScaleForDcCurrent() / 3276800.0

    def getCombinedKacoAcPowerHiRes(self):
        return self.__scaleForAcPower(self.__query("CombinedKacoAcPowerHiRes"))

    def getLoadAcPower(self):
        return self.__scaleForAcPower(self.__query("LoadAcPower"))

    def getACLoadkWhTotalAcc(self):
        return self.__scaleForAcEnergy(self.__query("ACLoadkWhTotalAcc"))

    def getTotalKacokWhTotalAcc(self):
        return self.__scaleForAcEnergy(self.__query("TotalKacokWhTotalAcc"))

    def getBatteryVolts(self):
        return self.__scaleForDcVolts(self.__query("BatteryVolts"))

    def getDCBatteryPower(self):
        return self.__scaleForDcPower(self.__query("DCBatteryPower"))

    def __query(self, name):
        address, dataType = map[name]
        format = types[dataType]["format"]
        words = types[dataType]["words"]
        rawBytes = self.__protocol.query(address, words - 1)
        return struct.unpack(format, rawBytes)[0]

    def __populateCommonScales(self):
        scale_mem = self.__protocol.query(41000, 5)
        self.__commonScaleForAcVolts = struct.unpack("<H", bytes(scale_mem[0:2]))[0]
        self.__commonScaleForAcCurrent = struct.unpack("<H", bytes(scale_mem[2:4]))[0]
        self.__commonScaleForDcVolts = struct.unpack("<H", bytes(scale_mem[4:6]))[0]
        self.__commonScaleForDcCurrent = struct.unpack("<H", bytes(scale_mem[6:8]))[0]
        self.__commonScaleForTemperature = struct.unpack("<H", bytes(scale_mem[8:10]))[0]
        self.__commonScaleForInternalVoltages = struct.unpack("<H", bytes(scale_mem[10:12]))
