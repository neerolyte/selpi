import binascii
from doctest import SKIP
from memory import Protocol, Range
from memory import sppro_addresses
import re
from memory import reduce
from memory import Data
import logging
import sys
from memory import extract
from memory import variable
from muster import Muster
from memory import convert
import struct

# TODO: work around for the way reduce() works and how many variables are involved
sys.setrecursionlimit(3000)

ADDRESSES = sppro_addresses.ADDRESSES
SKIP_VARS = ["Password", "CommPortActive"]

def add_parser(subparsers):
    parser = subparsers.add_parser('scan', help='scan known addresses')
    parser.set_defaults(func=run)

def run(args):
    protocol = Protocol()
    named_ranges = get_named_ranges()

    scales = get_scales()

    ranges = list(named_ranges.values())

    datas = []
    for range in reduce(ranges):
        logging.debug("query: %s" % range)
        res = protocol.query(range)
        datas.append(Data(range, res))

    for var_name in named_ranges:
        range = named_ranges[var_name]
        memory = extract(range, datas).bytes
        format_signed = "<h" if len(memory) == 2 else "<i"
        format_unsigned = "<H" if len(memory) == 2 else "<I"
        unscaled_unsigned = struct.unpack(format_unsigned, memory)[0]
        unscaled_signed = struct.unpack(format_signed, memory)[0]
        conversion = 'ac_wh' # TODO: pass in conversion as an argument
        print(
            var_name,
            binascii.hexlify(memory),
            convert(conversion, unscaled_signed, scales),
            convert(conversion, unscaled_unsigned, scales),
        )

def get_named_ranges():
    named_ranges = {}

    for var_name in ADDRESSES:
        if var_name in SKIP_VARS:
            continue
        # skip the second half of 2 word variables
        if re.search('HiWord', var_name):
            continue
        address = ADDRESSES[var_name]
        # TODO: these addresses break the Range class currently
        if address > 65535:
            continue
        words = 2 if re.search('LoWord', var_name) else 1
        named_ranges[var_name] = Range(address, words)

    return named_ranges

def get_scales():
    scale_variables = [
        variable.create('CommonScaleForAcVolts'),
        variable.create('CommonScaleForAcCurrent'),
        variable.create('CommonScaleForDcVolts'),
        variable.create('CommonScaleForDcCurrent'),
        variable.create('CommonScaleForTemperature'),
        variable.create('CommonScaleForInternalVoltages'),
    ]
    muster = Muster()
    muster.update(scale_variables)
    scales = {}
    for var in scale_variables:
        scales[var.get_name()] = var.get_value([])
    return scales
