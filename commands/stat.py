import json
import connection
from protocol import Protocol
from muster import Muster
import variable

def add_parser(subparsers):
    parser = subparsers.add_parser('stat', help='show known stats')
    parser.set_defaults(func=run)

def run(args):
    protocol = Protocol(connection.create())
    protocol.login()
    muster = Muster(protocol)

    scale_vars = muster.query([
        variable.create('CommonScaleForAcVolts'),
        variable.create('CommonScaleForAcCurrent'),
        variable.create('CommonScaleForDcVolts'),
        variable.create('CommonScaleForDcCurrent'),
        variable.create('CommonScaleForTemperature'),
        variable.create('CommonScaleForInternalVoltages'),
    ])
    scales = {}
    for var in scale_vars:
        scales[var.get_name()] = var.get_value([])

    variables = muster.query([
        variable.create('CombinedKacoAcPowerHiRes'),
        variable.create('Shunt1Name'),
        variable.create('Shunt1Power'),
        variable.create('Shunt2Name'),
        variable.create('Shunt2Power'),
        variable.create('BatteryVolts'),
        variable.create('BatteryTemperature'),
        variable.create('LoadAcPower'),
        variable.create('DCBatteryPower'),
        variable.create('ACLoadkWhTotalAcc'),
        variable.create('BattOutkWhPreviousAcc'),
        variable.create('BattSocPercent'),
    ])
    stats = []
    for var in variables:
        stats.append({
            "description": memory.MAP[var.get_name()][memory.DESCRIPTION],
            "name": var.get_name(),
            "value": "%s%s" % (var.get_value(scales), memory.MAP[var.get_name()][memory.UNITS]),
        })
    print(json.dumps(obj=stats, indent=2))
