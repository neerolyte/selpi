import json
from statistics import Statistics

statistics = Statistics()

def add_parser(subparsers):
    parser = subparsers.add_parser('stat-select', help='select.live stat emulation')
    parser.set_defaults(func=run)

def run(args):
    data = json.dumps(
        obj=statistics.get_select_emulated(),
        indent=2,
        separators=(',', ':')
    )
    print(data)
