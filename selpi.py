#!/usr/bin/env python
import argparse, pkgutil, importlib
import os, re
import commands
import logging
parser = argparse.ArgumentParser()

parser.add_argument(
    '--log',
    default = 'warning',
    choices = ['info','debug','warning','error','critical'],
    help='log level'
)

subparsers = parser.add_subparsers(help='command to run', metavar='{command}')
script_dir = os.path.dirname(os.path.realpath(__file__))

def get_commands() -> list:
    commands = []
    for _, _, files in os.walk(script_dir+'/commands'):
        for file in files:
            match = re.search('^([a-z-]+)\.py$', file)
            if not match:
                continue
            commands.append(match.group(1))
    commands.sort()
    return commands

for command_name in get_commands():
    importlib.import_module('commands.'+command_name)
    getattr(commands, command_name).add_parser(subparsers)

args = parser.parse_args()
logging.basicConfig(level=getattr(logging, args.log.upper()))

# Workaround required missing until 3.7 - https://docs.python.org/dev/library/argparse.html#sub-commands - how do I force virtual env to upgrade to 3.7?
if not hasattr(args, 'func'):
	parser.parse_args(['--help'])

args.func(args)
