from data import Data

def add_parser(subparsers):
    parser = subparsers.add_parser('stat', help='show known stats')
    parser.set_defaults(func=run)

def run(args):
    data = Data()
    print("Shunt1Power: %s" % data.get_scaled('Shunt1Power'))
    print("BatteryVolts: %s" % data.get_scaled('BatteryVolts'))
    print("BatteryTemperature: %s" % data.get_scaled('BatteryTemperature'))
    print("LoadAcPower: %s" % data.get_scaled('LoadAcPower'))
    print("DCBatteryPower: %s" % data.get_scaled('DCBatteryPower'))
    print("ACLoadkWhTotalAcc: %s" % data.get_scaled('ACLoadkWhTotalAcc'))
    print("BattOutkWhPreviousAcc: %s" % data.get_scaled('BattOutkWhPreviousAcc'))
