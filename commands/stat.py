from connection import *
from protocol import Protocol
import struct
from time import sleep

def add_parser(subparsers):
    parser = subparsers.add_parser('stat', help='show known stats')
    parser.set_defaults(func=run)

def run(args):
    #connection = ConnectionSerial() TODO: how do I make this dynamic?
    connection = ConnectionSelectLive()

    protocol = Protocol(connection)
    protocol.login()

    scale_mem = protocol.query(0xa028, 4)
    commonScaleForACVolts = struct.unpack("<H", bytes(scale_mem[0:2]))[0]
    commonScaleForACCurrent = struct.unpack("<H", bytes(scale_mem[2:4]))[0]
    commonScaleForDcVolts = struct.unpack("<H", bytes(scale_mem[4:6]))[0]
    commonScaleForDCCurrent = struct.unpack("<H", bytes(scale_mem[6:8]))[0]
    commonScaleForTemperature = struct.unpack("<H", bytes(scale_mem[8:10]))[0]
    print("commonScaleForACVolts: %s" % commonScaleForACVolts)
    print("commonScaleForACCurrent: %s" % commonScaleForACCurrent)
    print("commonScaleForDcVolts: %s" % commonScaleForDcVolts)
    print("commonScaleForDCCurrent: %s" % commonScaleForDCCurrent)
    print("commonScaleForTemperature: %s" % commonScaleForTemperature)

    # Solar Power - CombinedKacoAcPowerHiRes
    rb = protocol.query(0xa3a8, 1)
    solarPower = struct.unpack("<I", bytes(rb[0:4]))[0]
    solarPower = solarPower * commonScaleForACVolts * commonScaleForACCurrent / 26214400.0

    # Solar Energy - ACSolarKacokWhTotalAcc
    rb = protocol.query(0xa22f, 1)
    solarEnergy = struct.unpack("<I", bytes(rb[0:4]))[0]
    solarEnergy = solarEnergy * 24 * commonScaleForACVolts * commonScaleForACCurrent / 3276800.0

    # Load Power - LoadAcPower
    rb = protocol.query(0xa093, 1)
    loadPower = struct.unpack("<i", bytes(rb[0:4]))[0]
    loadPower = loadPower * commonScaleForACVolts * commonScaleForACCurrent / 26214400.0

    # Load Energy - ACLoadkWhTotalAcc
    rb = protocol.query(0xa1de, 1)
    loadEnergy = struct.unpack("<I", bytes(rb[0:4]))[0]
    loadEnergy = loadEnergy * 24 * commonScaleForACVolts * commonScaleForACCurrent / 3276800.0

    # Battery Volts - BatteryVolts
    rb = protocol.query(0xa05c, 0)
    batteryVolts = struct.unpack("<H", bytes(rb[0:2]))[0]
    batteryVolts = batteryVolts * commonScaleForDcVolts / 327680.0

    # Battery Power - DCBatteryPower
    rb = protocol.query(0xa02f, 1)
    dcBatteryPower = struct.unpack("<i", bytes(rb[0:4]))[0]
    dcBatteryPower = dcBatteryPower * commonScaleForDcVolts * commonScaleForDCCurrent / 3276800.0

    print("Solar Power: %sW" % solarPower)
    print("Solar Energy: %sWh" % solarEnergy)
    print("Load Power: %sW" % loadPower)
    print("Load Energy: %sWh" % loadEnergy)
    print("Battery Volts: %sV" % batteryVolts)
    print("Battery Power: %sW" % dcBatteryPower)
