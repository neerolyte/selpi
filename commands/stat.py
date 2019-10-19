def add_parser(subparsers):
	parser = subparsers.add_parser('stat', help='show known stats')
	parser.set_defaults(func=run)

def run(args):
	print("TODO")
