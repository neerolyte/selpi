from muster import Muster
from memory import variable
import time

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

    def get_select_emulated(self):
        vars = {
            "DCkWhInToday": variable.create("DCkWhInToday"),
            "BattInkWhTotalAcc": variable.create('BattInkWhTotalAcc'),
            "DCkWhOutToday": variable.create("DCkWhOutToday"),
            "BattOutkWhTotalAcc": variable.create('BattOutkWhTotalAcc'),
            "BattSocPercent": variable.create('BattSocPercent'),
            "Shunt1Power": variable.create('Shunt1Power'),
            "DCBatteryPower": variable.create('DCBatteryPower'),
            "LoadAcPower": variable.create('LoadAcPower'),
            "solarinverter_w": variable.create('CombinedKacoAcPowerHiRes'),
            "ACLoadkWhTotalAcc": variable.create("ACLoadkWhTotalAcc"),
            "ACInputWhTodayAcc": variable.create("ACInputWhTodayAcc"),
            "ACInputWhTotalAcc": variable.create("ACInputWhTotalAcc"),
            "ACExportWhTodayAcc": variable.create("ACExportWhTodayAcc"),
            "ACExportWhTotalAcc": variable.create("ACExportWhTotalAcc"),
            "ACLoadWhAcc": variable.create("ACLoadWhAcc"),
            "ACSolarWhTotalAcc": variable.create("ACSolarWhTotalAcc"),
            "Shunt1WhTotalAcc": variable.create("Shunt1WhTotalAcc"),
            "ACSolarWhTodayAcc": variable.create("ACSolarWhTodayAcc"),
            "Shunt1WhTodayAcc": variable.create("Shunt1WhTodayAcc"),
            "ACGeneratorPower": variable.create("ACGeneratorPower"),
        }
        self.__update(list(vars.values()))
        timestamp = int(time.time())
        items = {
            "battery_in_wh_today": vars["DCkWhInToday"].get_value(self.scales) / 1000,
            "battery_in_wh_total": vars["BattInkWhTotalAcc"].get_value(self.scales) / 1000,
            "battery_out_wh_today": vars["DCkWhOutToday"].get_value(self.scales) / 1000,
            "battery_out_wh_total": vars["BattOutkWhTotalAcc"].get_value(self.scales) / 1000,
            "battery_soc": vars["BattSocPercent"].get_value(self.scales),
            "battery_w": vars["DCBatteryPower"].get_value(self.scales),
            #"fault_code": 0,
            #"fault_ts": 0,
            #"gen_status": 0,
            "grid_in_wh_today": vars["ACInputWhTodayAcc"].get_value(self.scales) / 1000,
            "grid_in_wh_total": vars["ACInputWhTotalAcc"].get_value(self.scales) / 1000,
            "grid_out_wh_today": vars["ACExportWhTodayAcc"].get_value(self.scales) / 1000, # unverified guess
            "grid_out_wh_total": vars["ACExportWhTotalAcc"].get_value(self.scales) / 1000, # unverified guess
            "grid_w": vars["ACGeneratorPower"].get_value(self.scales),
            "load_w": vars["LoadAcPower"].get_value(self.scales),
            "load_wh_today": vars["ACLoadWhAcc"].get_value(self.scales) / 1000,
            "load_wh_total": vars["ACLoadkWhTotalAcc"].get_value(self.scales) / 1000,
            "shunt_w": 0 - vars["Shunt1Power"].get_value(self.scales),
            # TODO: assumes shunt 1 is always a solar shunt
            "solar_wh_today": ( vars["ACSolarWhTodayAcc"].get_value(self.scales) + 0 - vars["Shunt1WhTodayAcc"].get_value(self.scales)) / 1000,
            "solar_wh_total": (vars["ACSolarWhTotalAcc"].get_value(self.scales) + (0 -vars["Shunt1WhTotalAcc"].get_value(self.scales))) / 1000,
            "solarinverter_w": vars["solarinverter_w"].get_value(self.scales),
            "timestamp": timestamp,
        }
        return {
            "device": {
                "name": "Selectronic SP-PRO",
            },
            "item_count": len(items),
            "items": items,
            "comment": "energies are actually in kWh, not Wh",
            "now": timestamp
        }

    @property
    def scales(self):
        if not self.__scales:
            self.__scales = {}
            for variable in self.__scale_variables:
                self.__scales[variable.get_name()] = variable.get_value([])
        return self.__scales
