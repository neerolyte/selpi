from connection import ConnectionSerial
from protocol import Protocol
import struct
from time import sleep

def add_parser(subparsers):
	parser = subparsers.add_parser('stat', help='show known stats')
	parser.set_defaults(func=run)

def run(args):
    connection = ConnectionSerial()
    protocol = Protocol(connection)
    protocol.login()
    while True:
        scale_mem = protocol.query(0xa028, 7)
        commonScaleForDcVolts = struct.unpack("<H", bytes(scale_mem[4:6]))[0]
        print("commonScaleForDcVolts: %s" % commonScaleForDcVolts)
        bv_mem = protocol.query(0xa05c, 1)
        batteryVolts = struct.unpack("<H", bytes(bv_mem[0:2]))[0]
        batteryVolts = batteryVolts * commonScaleForDcVolts / 327680.0
        print("Battery V: %s" % batteryVolts)
        sleep(1)
