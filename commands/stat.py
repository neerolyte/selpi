import json
import connection
from memory import Protocol
from muster import Muster
from memory import variable

def add_parser(subparsers):
    parser = subparsers.add_parser('stat', help='show known stats')
    parser.set_defaults(func=run)

def run(args):
    protocol = Protocol(connection.create())
    protocol.login()
    muster = Muster(protocol)

    scale_vars = [
        variable.create('CommonScaleForAcVolts'),
        variable.create('CommonScaleForAcCurrent'),
        variable.create('CommonScaleForDcVolts'),
        variable.create('CommonScaleForDcCurrent'),
        variable.create('CommonScaleForTemperature'),
        variable.create('CommonScaleForInternalVoltages'),
    ]
    variables = [
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
    ]

    muster.update(scale_vars + variables)

    scales = {}
    for var in scale_vars:
        scales[var.get_name()] = var.get_value([])

    stats = []
    for var in variables:
        stats.append({
            "description": variable.MAP[var.get_name()][variable.DESCRIPTION],
            "name": var.get_name(),
            "value": "%s%s" % (var.get_value(scales), variable.MAP[var.get_name()][variable.UNITS]),
        })
    print(json.dumps(obj=stats, indent=2))
