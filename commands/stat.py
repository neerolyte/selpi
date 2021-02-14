from data import Data

def add_parser(subparsers):
    parser = subparsers.add_parser('stat', help='show known stats')
    parser.set_defaults(func=run)

def run(args):
    data = Data()
    print("CombinedKacoAcPowerHiRes: %s" % data.get_scaled('CombinedKacoAcPowerHiRes'))
    print("Shunt1Name: %s" % data.get_scaled('Shunt1Name'))
    print("Shunt1Power: %s" % data.get_scaled('Shunt1Power'))
    print("Shunt2Name: %s" % data.get_scaled('Shunt2Name'))
    print("Shunt2Power: %s" % data.get_scaled('Shunt2Power'))
    print("BatteryVolts: %s" % data.get_scaled('BatteryVolts'))
    print("BatteryTemperature: %s" % data.get_scaled('BatteryTemperature'))
    print("LoadAcPower: %s" % data.get_scaled('LoadAcPower'))
    print("DCBatteryPower: %s" % data.get_scaled('DCBatteryPower'))
    print("ACLoadkWhTotalAcc: %s" % data.get_scaled('ACLoadkWhTotalAcc'))
    print("BattOutkWhPreviousAcc: %s" % data.get_scaled('BattOutkWhPreviousAcc'))
    print("BattSocPercent: %s" % data.get_scaled('BattSocPercent'))
