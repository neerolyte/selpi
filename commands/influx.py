from memory import variable
from statistics import Statistics
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
import datetime
import time
import settings
import json
from muster import Muster

schema = []

def add_parser(subparsers):
    parser = subparsers.add_parser('influx', help='start influxdb writer')
    parser.set_defaults(func=run)

def run(args):
    InfluxWriter().start()

def _parse_variable_groups():
    raw_groups = json.loads(settings.getb(b'INFLUX_VARIABLE_GROUPS'))
    groups = []
    for raw_group in raw_groups:
        variables = []
        for variable_name in raw_group['variables']:
            variables.append(variable.create(variable_name))
        groups.append({
            'measurement': raw_group['measurement'],
            'frequency': raw_group['frequency'],
            'variables': variables,
        })
    return groups


class InfluxWriter():
    def __init__(self):
        self.__variables_groups = _parse_variable_groups()
        self.__influx_client = None
        # TODO: Figure out how to recombine with Statistics
        self.__muster = Muster()
        self.__scale_variables = [
            variable.create('CommonScaleForAcVolts'),
            variable.create('CommonScaleForAcCurrent'),
            variable.create('CommonScaleForDcVolts'),
            variable.create('CommonScaleForDcCurrent'),
            variable.create('CommonScaleForTemperature'),
            variable.create('CommonScaleForInternalVoltages'),
        ]
        self.__scales = None

    def start(self):
        while True:
            self.__update()
            sleep_duration = self.__get_sleep_duration()
            if sleep_duration > 0:
                print("Sleeping for %s" % sleep_duration)
                time.sleep(sleep_duration)

    def __update(self):
        for group in self.__variables_groups:
            self.__update_group(group)

    def __get_sleep_duration(self):
        next_updates = []
        for group in self.__variables_groups:
            next_updates.append(self.__get_next_update(group))
        return min(next_updates) - time.monotonic()

    def __update_group(self, group):
        current_time = time.monotonic()
        if self.__get_next_update(group) > current_time:
            return
        self.__update_variables(group['variables'])
        group['last_update'] = current_time
        self.influx_client.write_points([self.__get_points(group)])

    def __get_next_update(self, group):
        if not 'last_update' in group:
            return 0
        return group['last_update'] + group['frequency']

    def __get_points(self, group):
        point = {
            'measurement': group['measurement'],
            'tags': {},
            'time': datetime.datetime.now().isoformat(),
            'fields': self.__get_fields(group),
        }
        print(point)
        return point

    def __get_fields(self, group):
        fields = {}
        for var in group['variables']:
            fields[var.get_name()] = var.get_value(self.scales)
        return fields

    @property
    def influx_client(self) -> InfluxDBClient:
        if not self.__influx_client:
            self.__influx_client = InfluxDBClient(host='influxdb', port=8086)
            self.__influx_client.create_database('selpi')
            self.__influx_client.switch_database('selpi')
        return self.__influx_client

    def __update_variables(self, variables):
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
