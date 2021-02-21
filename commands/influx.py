from statistics import Statistics
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
import datetime
import time

schema = []

def add_parser(subparsers):
    parser = subparsers.add_parser('influx', help='start influxdb writer')
    parser.set_defaults(func=run)

def run(args):
    InfluxWriter().start()

class InfluxWriter():
    def __init__(self):
        self.__statistics = Statistics()
        self.__client = None

    def start(self):
        while True:
            self.client.write_points([self.__get_point()])
            time.sleep(2)

    def __get_point(self):
        point = {
            'measurement': 'point',
            'tags': {},
            'time': datetime.datetime.now().isoformat(),
            'fields': self.__get_fields(),
        }
        print(point)
        return point

    def __get_fields(self):
        stats = self.__statistics.get()
        fields = {}
        for stat in stats:
            fields[stat['name']] = stat['value']
        return fields

    @property
    def client(self):
        if not self.__client:
            self.__client = InfluxDBClient(host='influxdb', port=8086)
            self.__client.create_database('selpi')
            self.__client.switch_database('selpi')
        return self.__client
