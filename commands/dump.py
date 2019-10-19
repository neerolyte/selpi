def add_parser(subparsers):
	parser = subparsers.add_parser('dump', help='dump memory to stdout')
	parser.set_defaults(func=run)

def run(args):
	login()

	# Before 0xa001 we don't get anything back
	start=0xa001
	# How much to get at a time (also tied to console line length currently)
	length=0x10
	# When to stop
	end=0xa2ff
	for address in range(start, end, length):
		hexaddy = binascii.hexlify(struct.pack(">H", address))
		mem = binascii.hexlify(get(address, length))
		print(b''.join([b'0x',hexaddy,b' ',mem]).decode('utf-8'))

import serial, time, struct, hashlib, binascii, config
from crc import CRC
from config import Config

# Initialise USB port
SPPort = serial.Serial(Config().get('port'), baudrate=Config().get('baudrate'), timeout=0.5)
SPPort.flushOutput()

def calculateCRCI(msg):
    return CRC(msg).as_int()

def calculateCRC(msg):
    return CRC(msg).as_bytes()

def getReadRequest(address, length):
    m = bytearray([ord("Q"), length])
    m.extend(struct.pack("<I", address))
    m.extend(calculateCRC(m))
    return m

def getWriteRequest(address, data):
    m = bytearray([ord("W"), len(data)-1])
    m.extend(struct.pack("<I", address))
    m.extend(calculateCRC(m))

    # Convert data from int[] to byte[], little endian but reversing the byte order (thanks Selectronic :( )
    ba = bytearray()
    for x in data:
        bb = bytearray(struct.pack("<I", x)[0:2])
        bb.reverse()
        ba.extend(bb)

    m.extend(ba)
    m.extend(calculateCRC(ba))
    return m

def login():

    # Get hash from SP Pro
    h = doReadRequest(0x1f0000, 7)[8:24]

    # Compute MD5 hash to send back, including login password
    h.extend(Config().get('password').ljust(32).encode("ascii"))

    # Compute md5
    md5 = bytearray(hashlib.md5(h).digest())

    # Convert md5 to little endian int32 array
    md5ia = []
    for i in range(0, len(md5), 2):
        md5ia.extend(struct.unpack("<I", bytes(md5[i:i+2] + bytearray([0, 0]))))

    # Respond with hash/pwd MD5
    r = getWriteRequest(0x1f0000, md5ia)
    SPPort.write(r)
    responseBuffer = bytearray()
    for i in range(1, 52):
        responseBuffer.extend(SPPort.read())
        if len(responseBuffer) == 26:
            return True

    return False

def doReadRequest(address, length):
    r = getReadRequest(address, length)
    SPPort.write(r)
    SPPort.flushOutput()
    responseBuffer = bytearray()
    expectedResponseLength = 2 * (length + 1) + 10
    for i in range(1, expectedResponseLength + 10): # Allow for a few timeouts @ 0.5s
        responseBuffer.extend(SPPort.read())
        if len(responseBuffer) == expectedResponseLength:
            break
    if calculateCRCI(responseBuffer) != 0:
        responseBuffer = bytearray()
    return responseBuffer # If it fails and just times out, will be empty (or if it fails CRC)
    
def get(address, length):
    r = getReadRequest(address, length)
    responseBuffer = doReadRequest(address, length)
    return responseBuffer[len(r):len(r)+2*(length)]
