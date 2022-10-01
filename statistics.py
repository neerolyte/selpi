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
            "battery_in_wh_today": variable.create("DCkWhInToday"),
            "battery_in_wh_total": variable.create('BattInkWhTotalAcc'),
            "battery_out_wh_today": variable.create("DCkWhOutToday"),
            "battery_out_wh_total": variable.create('BattOutkWhTotalAcc'),
            "battery_soc": variable.create('BattSocPercent'),
            "shunt_w_negated": variable.create('Shunt1Power'),
            "battery_w": variable.create('DCBatteryPower'),
            "load_w": variable.create('LoadAcPower'),
            "grid_w": variable.create('ACGeneratorPower'),
            "solarinverter_w": variable.create('CombinedKacoAcPowerHiRes'),
            "load_wh_total": variable.create("ACLoadkWhTotalAcc"),
            "grid_in_wh_total": variable.create("ACInputWhTotalAcc"),
        }
        self.__update(list(vars.values()))
        timestamp = int(time.time())
        items = {
            "battery_in_wh_today": vars["battery_in_wh_today"].get_value(self.scales) / 1000,
            "battery_in_wh_total": vars["battery_in_wh_total"].get_value(self.scales) / 1000,
            "battery_out_wh_today": vars["battery_out_wh_today"].get_value(self.scales) / 1000,
            "battery_out_wh_total": vars["battery_out_wh_total"].get_value(self.scales) / 1000,
            "battery_soc": vars["battery_soc"].get_value(self.scales),
            "battery_w": vars["battery_w"].get_value(self.scales),
            #"fault_code": 0,
            #"fault_ts": 0,
            #"gen_status": 0,
            #"grid_in_wh_today":0.0,
            "grid_in_wh_total": vars["grid_in_wh_total"].get_value(self.scales) / 1000,
            #"grid_out_wh_today":0.0,
            #"grid_out_wh_total":0.0,
            "grid_w": vars["grid_w"].get_value(self.scales),
            "load_w": vars["load_w"].get_value(self.scales),
            #"load_wh_today": vars["load_wh_today"].get_value(self.scales) / 1000,
            "load_wh_total": vars["load_wh_total"].get_value(self.scales) / 1000,
            "shunt_w": 0 - vars["shunt_w_negated"].get_value(self.scales),
            #"solar_wh_today":0,
            #"solar_wh_total":0,
            "solarinverter_w": vars["solarinverter_w"].get_value(self.scales),
            "timestamp": timestamp,
        }
        return {
            "device": {
                "name": "Selectronic SP-PRO",
            },
            "item_count": len(items),
            "items": items,
            "now": timestamp
        }

    @property
    def scales(self):
        if not self.__scales:
            self.__scales = {}
            for variable in self.__scale_variables:
                self.__scales[variable.get_name()] = variable.get_value([])
        return self.__scales
