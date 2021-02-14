import struct
import sys
from error import Error

def create(arg):
    if type(arg) is str:
        return Variable(arg, MAP[arg][ADDRESS])
    if type(arg) is int:
        return Variable(address_to_name(arg), arg)
    raise NotImplementedError("Unable to create Variable from %s" % type(arg))

def address_to_name(address):
    for name in MAP.keys():
        if MAP[name][ADDRESS] == address:
            return name
    return 'Unknown'

ADDRESS = 'address'
TYPE = 'type'
DESCRIPTION = 'description'
UNITS = 'units'
CONVERSION = 'conversion'
FORMAT = 'format'
WORDS = 'words'

MAP = {
    "CommonScaleForAcVolts": {
        ADDRESS: 41000,
        TYPE: "ushort",
    },
    "CommonScaleForAcCurrent": {
        ADDRESS: 41001,
        TYPE: "ushort",
    },
    "CommonScaleForDcVolts": {
        ADDRESS: 41002,
        TYPE: "ushort",
    },
    "CommonScaleForDcCurrent": {
        ADDRESS: 41003,
        TYPE: "ushort",
    },
    "CommonScaleForTemperature": {
        ADDRESS: 41004,
        TYPE: "ushort",
    },
    "CommonScaleForInternalVoltages": {
        ADDRESS: 41005,
        TYPE: "ushort",
    },
    "TotalKacokWhTotalAcc": {
        DESCRIPTION: 'AC Lifetime Solar Energy',
        ADDRESS: 41519,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "ac_wh",
    },
    "CombinedKacoAcPowerHiRes": {
        DESCRIPTION: 'AC Solar Power',
        ADDRESS: 41896,
        TYPE: "uint",
        UNITS: "W",
        CONVERSION: "ac_w",
    },
    "LoadAcPower": {
        DESCRIPTION: 'AC Load Power',
        ADDRESS: 41107,
        TYPE: "uint",
        UNITS: "W",
        CONVERSION: "ac_w",
    },
    "ACLoadkWhTotalAcc": {
        DESCRIPTION: 'AC Lifetime Load Energy',
        ADDRESS: 41438,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "ac_wh",
    },
    "BatteryVolts": {
        DESCRIPTION: 'Battery Volts',
        ADDRESS: 0xa05c,
        TYPE: "ushort",
        UNITS: "V",
        CONVERSION: "dc_v",
    },
    "DCBatteryPower": {
        DESCRIPTION: 'Battery Power',
        ADDRESS: 41007,
        TYPE: "int",
        UNITS: "W",
        CONVERSION: "dc_w",
    },
    "Shunt1Power": {
        DESCRIPTION: 'Shunt 1 Power',
        ADDRESS: 0xa088,
        TYPE: "short",
        UNITS: "W",
        CONVERSION: "dc_w",
    },
    "Shunt2Power": {
        DESCRIPTION: 'Shunt 2 Power',
        ADDRESS: 0xa089,
        TYPE: "short",
        UNITS: "W",
        CONVERSION: "dc_w",
    },
    "Shunt1Name": {
        DESCRIPTION: 'Shunt 1 Name',
        ADDRESS: 49417,
        TYPE: "short",
        UNITS: "",
        CONVERSION: "shunt_name",
    },
    "Shunt2Name": {
        DESCRIPTION: 'Shunt 2 Name',
        ADDRESS: 49418,
        TYPE: "short",
        UNITS: "",
        CONVERSION: "shunt_name",
    },
    "BatteryTemperature": {
        DESCRIPTION: "Battery Temperature",
        ADDRESS: 0xa03c,
        TYPE: "ushort",
        UNITS: "°C",
        CONVERSION: "temperature",
    },
    "BattOutkWhPreviousAcc": {
        DESCRIPTION: "Battery Out Energy Today",
        ADDRESS: 41356,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattSocPercent": {
        DESCRIPTION: "Battery State of Charge",
        ADDRESS: 41089,
        TYPE: "ushort",
        UNITS: "%",
        CONVERSION: "percent",
    },
}

# Magic constants used for shifting integers to floating point numbers
MAGIC = 32768.0
MAGIC_AC_W_DIVISOR        = MAGIC * 800.0
MAGIC_DC_W_DIVISOR        = MAGIC * 100.0
MAGIC_DC_V_DIVISOR        = MAGIC * 10.0
MAGIC_WH_MULTIPLIER       = 24.0
MAGIC_WH_DIVISOR          = MAGIC * 100.0
MAGIC_TEMPERATURE_DIVISOR = MAGIC
MAGIC_PERCENT_DIVISOR     = 256.0

SHUNT_NAMES = {
    0: 'None',
    1: 'Solar',
    2: 'Wind',
    3: 'Hydro',
    4: 'Charger',
    5: 'Load',
    6: 'Dual',
    7: 'Multiple SP PROs',
    8: 'Log Only',
    9: 'System SoC',
    10: 'Direct SoC Input',
}

TYPES = {
    "ushort": {
        FORMAT: "<H",
        WORDS: 1,
    },
    "short": {
        FORMAT: "<h",
        WORDS: 1,
    },
    "uint": {
        FORMAT: "<I",
        WORDS: 2,
    },
    "int": {
        FORMAT: "<i",
        WORDS: 2,
    },
}

def _convert_ac_w(raw, scales):
    return raw * scales['CommonScaleForAcVolts'] * scales['CommonScaleForAcCurrent'] / MAGIC_AC_W_DIVISOR

def _convert_ac_wh(raw, scales):
    return raw * MAGIC_WH_MULTIPLIER * scales['CommonScaleForAcVolts'] * scales['CommonScaleForAcCurrent'] / MAGIC_WH_DIVISOR

def _convert_dc_w(raw, scales):
    return raw * scales['CommonScaleForDcVolts'] * scales['CommonScaleForDcCurrent'] / MAGIC_DC_W_DIVISOR

def _convert_dc_wh(raw, scales):
    return raw * MAGIC_WH_MULTIPLIER * scales['CommonScaleForDcVolts'] * scales['CommonScaleForDcCurrent'] / MAGIC_WH_DIVISOR

def _convert_dc_v(raw, scales):
    return raw * scales['CommonScaleForDcVolts'] / MAGIC_DC_V_DIVISOR

def _convert_temperature(raw, scales):
    return raw * scales['CommonScaleForTemperature'] / MAGIC_TEMPERATURE_DIVISOR

def _convert_percent(raw, scales):
    return raw / MAGIC_PERCENT_DIVISOR

def _convert_shunt_name(raw, scales):
    if raw in SHUNT_NAMES:
        return SHUNT_NAMES[raw]
    return 'Error'

class Variable:
    def __init__(self, name: str, address: int, bytes: bytes=b'\x00\x00'):
        self.__name = name
        self.__address = address
        self.__bytes = bytes

    def get_address(self):
        return self.__address

    def get_name(self):
        return self.__name

    """
    Get the number of words this variables takes up in memory
    """
    def get_words(self):
        return TYPES[self.get_type()][WORDS]

    def get_type(self):
        if not self.__name in MAP:
            return 'ushort'
        return MAP[self.__name][TYPE]

    """
    Create a new Varible with the supplied value
    """
    def set_bytes(self, bytes):
        return Variable(self.__name, self.__address, bytes)

    def get_bytes(self):
        return self.__bytes

    """
    Get the converted value
    """
    def get_value(self, scales: dict):
        if not self.is_known():
            raise Error("Can not convert value for unknown variable type")
        mem_info = MAP[self.__name]
        type_info = TYPES[self.get_type()]
        format = type_info["format"]
        words = type_info[WORDS]
        unscaled = struct.unpack(format, self.__bytes)[0]
        if not CONVERSION in mem_info:
            return unscaled
        scaleMethod = getattr(sys.modules[__name__], '_convert_'+mem_info[CONVERSION])
        return scaleMethod(unscaled, scales)

    def is_known(self):
        return self.__name in MAP
