#!/usr/bin/env python
import argparse, pkgutil, importlib

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='command to run', metavar='{command}')

command_names = ['dump', 'hello', 'stat']

import commands

for command_name in command_names:
    importlib.import_module('commands.'+command_name)
    getattr(commands, command_name).add_parser(subparsers)

args = parser.parse_args()

# Workaround required missing until 3.7 - https://docs.python.org/dev/library/argparse.html#sub-commands - how do I force virtual env to upgrade to 3.7?
if not hasattr(args, 'func'):
	parser.parse_args(['--help'])

args.func(args)
