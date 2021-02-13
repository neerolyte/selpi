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
    # "Name": [address, type, units],
    "CommonScaleForAcVolts": [41000, "ushort", "Unit"],
    "CommonScaleForAcCurrent": [41001, "ushort", "Unit"],
    "CommonScaleForDcVolts": [41002, "ushort", "Unit"],
    "CommonScaleForDcCurrent": [41003, "ushort", "Unit"],
    "CommonScaleForTemperature": [41004, "ushort", "Unit"],
    "CommonScaleForInternalVoltages": [41005, "ushort", "Unit"],
    "TotalKacokWhTotalAcc": [41519, "uint", "AcEnergy"],
    "CombinedKacoAcPowerHiRes": [41896, "uint", "AcPower"],
    "LoadAcPower": [41107, "uint", "AcPower"],
    "ACLoadkWhTotalAcc": [41438, "uint", "AcEnergy"],
    "BatteryVolts": [41052, "ushort", "DcVolts"],
    "DCBatteryPower": [41007, "uint", "DcPower"],
}

def _unpack(format, bytes):
    return struct.unpack(format, bytes)[0]

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

    def __getCommonScaleForAcVolts(self):
        if self.__commonScaleForAcVolts == None:
            self.__populateCommonScales()
        return self.__commonScaleForAcVolts

    def __getCommonScaleForAcCurrent(self):
        if self.__commonScaleForAcCurrent == None:
            self.__populateCommonScales()
        return self.__commonScaleForAcCurrent

    def __getCommonScaleForDcVolts(self):
        if self.__commonScaleForDcVolts == None:
            self.__populateCommonScales()
        return self.__commonScaleForDcVolts

    def __getCommonScaleForDcCurrent(self):
        if self.__commonScaleForDcCurrent == None:
            self.__populateCommonScales()
        return self.__commonScaleForDcCurrent

    def _scaleForAcPower(self, unscaledPower):
        return unscaledPower * self.__getCommonScaleForAcVolts() * self.__getCommonScaleForAcCurrent() / 26214400.0

    def _scaleForAcEnergy(self, unscaledEnergy):
        return unscaledEnergy * 24 * self.__getCommonScaleForAcVolts() * self.__getCommonScaleForAcCurrent() / 3276800.0

    def _scaleForDcVolts(self, unscaledVolts):
        return unscaledVolts * self.__getCommonScaleForDcVolts() / 327680.0

    def _scaleForDcPower(self, unscaledPower):
        return unscaledPower * self.__getCommonScaleForDcVolts() * self.__getCommonScaleForDcCurrent() / 3276800.0

    def getCombinedKacoAcPowerHiRes(self):
        return self.__query("CombinedKacoAcPowerHiRes")

    def getLoadAcPower(self):
        return self.__query("LoadAcPower")

    def getACLoadkWhTotalAcc(self):
        return self.__query("ACLoadkWhTotalAcc")

    def getTotalKacokWhTotalAcc(self):
        return self.__query("TotalKacokWhTotalAcc")

    def getBatteryVolts(self):
        return self.__query("BatteryVolts")

    def getDCBatteryPower(self):
        return self.__query("DCBatteryPower")

    def __query(self, name):
        address, dataType, unit = map[name]
        format = types[dataType]["format"]
        words = types[dataType]["words"]
        rawBytes = self.__protocol.query(address, words - 1)
        unscaled = _unpack(format, rawBytes)
        scaleMethod = getattr(self, '_scaleFor'+unit)
        return scaleMethod(unscaled)

    def __populateCommonScales(self):
        address, dataType, unit = map["CommonScaleForAcVolts"]
        format = types[dataType]["format"]
        scale_mem = self.__protocol.query(address, 5)
        self.__commonScaleForAcVolts = _unpack(format, scale_mem[0:2])
        self.__commonScaleForAcCurrent = _unpack(format, scale_mem[2:4])
        self.__commonScaleForDcVolts = _unpack(format, scale_mem[4:6])
        self.__commonScaleForDcCurrent = _unpack(format, scale_mem[6:8])
        self.__commonScaleForTemperature = _unpack(format, scale_mem[8:10])
        self.__commonScaleForInternalVoltages = _unpack(format, scale_mem[10:12])
