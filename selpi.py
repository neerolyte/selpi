#!/usr/bin/env python
import argparse, pkgutil

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='command to run', metavar='{command}')

import commands.dump
commands.dump.add_parser(subparsers)
import commands.stat
commands.stat.add_parser(subparsers)

args = parser.parse_args()

# Workaround required missing until 3.7 - https://docs.python.org/dev/library/argparse.html#sub-commands - how do I force virtual env to upgrade to 3.7?
if not hasattr(args, 'func'):
	parser.parse_args(['--help'])

args.func(args)