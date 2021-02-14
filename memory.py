import struct
import sys

DESCRIPTION = 'description'
ADDRESS = 'address'
TYPE = 'type'
UNITS = 'units'
SCALE = 'scale'
WORDS = 'words'
FORMAT = 'format'

# Magic constants used for shifting integers to floating point numbers
MAGIC = 32768.0
MAGIC_AC_W_DIVISOR        = MAGIC * 800.0
MAGIC_DC_W_DIVISOR        = MAGIC * 100.0
MAGIC_DC_V_DIVISOR        = MAGIC * 10.0
MAGIC_WH_MULTIPLIER       = 24.0
MAGIC_WH_DIVISOR          = MAGIC * 100.0
MAGIC_TEMPERATURE_DIVISOR = MAGIC
MAGIC_PERCENT_DIVISOR     = 256.0

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
        SCALE: "ac_wh",
    },
    "CombinedKacoAcPowerHiRes": {
        DESCRIPTION: 'AC Solar Power',
        ADDRESS: 41896,
        TYPE: "uint",
        UNITS: "W",
        SCALE: "ac_w",
    },
    "LoadAcPower": {
        DESCRIPTION: 'AC Load Power',
        ADDRESS: 41107,
        TYPE: "uint",
        UNITS: "W",
        SCALE: "ac_w",
    },
    "ACLoadkWhTotalAcc": {
        DESCRIPTION: 'AC Lifetime Load Energy',
        ADDRESS: 41438,
        TYPE: "uint",
        UNITS: "Wh",
        SCALE: "ac_wh",
    },
    "BatteryVolts": {
        DESCRIPTION: 'Battery Volts',
        ADDRESS: 0xa05c,
        TYPE: "ushort",
        UNITS: "V",
        SCALE: "dc_v",
    },
    "DCBatteryPower": {
        DESCRIPTION: 'Battery Power',
        ADDRESS: 41007,
        TYPE: "int",
        UNITS: "W",
        SCALE: "dc_w",
    },
    "Shunt1Power": {
        DESCRIPTION: 'Shunt 1 Power',
        ADDRESS: 0xa088,
        TYPE: "short",
        UNITS: "W",
        SCALE: "dc_w",
    },
    "Shunt2Power": {
        DESCRIPTION: 'Shunt 2 Power',
        ADDRESS: 0xa089,
        TYPE: "short",
        UNITS: "W",
        SCALE: "dc_w",
    },
    "Shunt1Name": {
        DESCRIPTION: 'Shunt 1 Name',
        ADDRESS: 49417,
        TYPE: "short",
        UNITS: "",
        SCALE: "shunt_name",
    },
    "Shunt2Name": {
        DESCRIPTION: 'Shunt 2 Name',
        ADDRESS: 49418,
        TYPE: "short",
        UNITS: "",
        SCALE: "shunt_name",
    },
    "BatteryTemperature": {
        DESCRIPTION: "Battery Temperature",
        ADDRESS: 0xa03c,
        TYPE: "ushort",
        UNITS: "°C",
        SCALE: "temperature",
    },
    "BattOutkWhPreviousAcc": {
        DESCRIPTION: "Battery Out Energy Today",
        ADDRESS: 41356,
        TYPE: "uint",
        UNITS: "Wh",
        SCALE: "dc_wh",
    },
    "BattSocPercent": {
        DESCRIPTION: "Battery State of Charge",
        ADDRESS: 41089,
        TYPE: "ushort",
        UNITS: "%",
        SCALE: "percent",
    },
}

def get_type(name):
    return MAP[name][TYPE]

def get_address(name):
    return MAP[name][ADDRESS]

def get_units(name):
    if UNITS in MAP[name]:
        return MAP[name][UNITS]
    return None

def scale(name, bytes, scales):
        mem_info = MAP[name]
        type = mem_info[TYPE]
        type_info = TYPES[type]
        format = type_info["format"]
        words = type_info[WORDS]
        unscaled = struct.unpack(format, bytes)[0]
        if not SCALE in mem_info:
            return unscaled
        scaleMethod = getattr(sys.modules[__name__], '_scale_for_'+mem_info[SCALE])
        return scaleMethod(unscaled, scales)

def _scale_for_ac_w(unscaled, scales):
    return unscaled * scales['CommonScaleForAcVolts'] * scales['CommonScaleForAcCurrent'] / MAGIC_AC_W_DIVISOR

def _scale_for_ac_wh(unscaled, scales):
    return unscaled * MAGIC_WH_MULTIPLIER * scales['CommonScaleForAcVolts'] * scales['CommonScaleForAcCurrent'] / MAGIC_WH_DIVISOR

def _scale_for_dc_w(unscaled, scales):
    return unscaled * scales['CommonScaleForDcVolts'] * scales['CommonScaleForDcCurrent'] / MAGIC_DC_W_DIVISOR

def _scale_for_dc_wh(unscaled, scales):
    return unscaled * MAGIC_WH_MULTIPLIER * scales['CommonScaleForDcVolts'] * scales['CommonScaleForDcCurrent'] / MAGIC_WH_DIVISOR

def _scale_for_dc_v(unscaled, scales):
    return unscaled * scales['CommonScaleForDcVolts'] / MAGIC_DC_V_DIVISOR

def _scale_for_temperature(unscaled, scales):
    return unscaled * scales['CommonScaleForTemperature'] / MAGIC_TEMPERATURE_DIVISOR

def _scale_for_percent(unscaled, scales):
    return unscaled / MAGIC_PERCENT_DIVISOR

def _scale_for_shunt_name(unscaled, scales):
    if unscaled in SHUNT_NAMES:
        return SHUNT_NAMES[unscaled]
    return 'Error'
