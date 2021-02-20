import json
from statistics import Statistics

def add_parser(subparsers):
    parser = subparsers.add_parser('stat', help='show known stats')
    parser.set_defaults(func=run)

def run(args):
    statistics = Statistics()
    print(json.dumps(obj=statistics.get(), indent=2))
