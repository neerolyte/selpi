from muster import Muster
from memory import variable

class Statistics():
    def __init__(self):
        self.__muster = Muster()
        self.__scale_variables = [
            variable.create('CommonScaleForAcVolts'),
            variable.create('CommonScaleForAcCurrent'),
            variable.create('CommonScaleForDcVolts'),
            variable.create('CommonScaleForDcCurrent'),
            variable.create('CommonScaleForTemperature'),
            variable.create('CommonScaleForInternalVoltages'),
        ]
        self.__variables = [
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
            variable.create('StatOfChargeShutdownSoC'),
        ]
        self.__scales = None

    def __update(self, variables):
        # opportunistically request scales if they're missing during another
        # request
        if not self.__scales:
            variables = variables + self.__scale_variables

        self.__muster.update(variables)

    def get(self):
        self.__update(self.__variables)
        stats = []
        for var in self.__variables:
            stats.append({
                "description": variable.MAP[var.get_name()][variable.DESCRIPTION],
                "name": var.get_name(),
                "value": var.get_value(self.scales),
                "units": variable.MAP[var.get_name()][variable.UNITS],
            })
        return stats

    @property
    def scales(self):
        if not self.__scales:
            self.__scales = {}
            for variable in self.__scale_variables:
                self.__scales[variable.get_name()] = variable.get_value([])
        return self.__scales
