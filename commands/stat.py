from data import Data

def add_parser(subparsers):
    parser = subparsers.add_parser('stat', help='show known stats')
    parser.set_defaults(func=run)

def run(args):
    data = Data()
    print("Solar Power: %sW" % data.getCombinedKacoAcPowerHiRes())
    print("Solar Energy: %sWh" % data.getTotalKacokWhTotalAcc())
    print("Load Power: %sW" % data.getLoadAcPower())
    print("Load Energy: %sWh" % data.getACLoadkWhTotalAcc())
    print("Battery Volts: %sV" % data.getBatteryVolts())
    print("Battery Power: %sW" % data.getDCBatteryPower())
