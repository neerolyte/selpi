from data import Data
import json
import memory

def add_parser(subparsers):
    parser = subparsers.add_parser('stat', help='show known stats')
    parser.set_defaults(func=run)

def run(args):
    data = Data()
    names = [
        'CombinedKacoAcPowerHiRes',
        'Shunt1Name',
        'Shunt1Power',
        'Shunt2Name',
        'Shunt2Power',
        'BatteryVolts',
        'BatteryTemperature',
        'LoadAcPower',
        'DCBatteryPower',
        'ACLoadkWhTotalAcc',
        'BattOutkWhPreviousAcc',
        'BattSocPercent',
    ]
    stats = []
    for name in names:
        stats.append({
            "description": memory.MAP[name][memory.DESCRIPTION],
            "name": name,
            "value": "%s%s" % (data.get_scaled(name), memory.MAP[name][memory.UNITS]),
        })
    print(json.dumps(obj=stats, indent=2))
