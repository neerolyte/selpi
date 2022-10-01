import struct
import sys

"""
Convert from inverter integers to local types
"""
def convert(conversion: str, value: int, scales: dict):
    method = getattr(sys.modules[__name__], '_convert_'+conversion)
    return method(value, scales)

# Magic constants used for shifting integers to floating point numbers
MAGIC = 32768.0
MAGIC_AC_W_DIVISOR        = MAGIC * 800.0
MAGIC_AC_W_SIGNED_DIVISOR = MAGIC * 100.0
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

def _convert_ac_w(raw, scales):
    return raw * scales['CommonScaleForAcVolts'] * scales['CommonScaleForAcCurrent'] / MAGIC_AC_W_DIVISOR

def _convert_ac_w_signed(raw, scales):
    return raw * scales['CommonScaleForAcVolts'] * scales['CommonScaleForAcCurrent'] / MAGIC_AC_W_SIGNED_DIVISOR

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
