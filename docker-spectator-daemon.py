#!/usr/bin/env python

from libs.classes.DockerSpeactatorDaemon import DockerSpectatorDaemon
from config import config
from argparse import ArgumentParser

# region Arguments parsing
parser = ArgumentParser()

commandGroup = parser.add_mutually_exclusive_group()
commandGroup.add_argument('--start', help='Start daemon', action='store_true')
commandGroup.add_argument('--stop', help='Stop daemon', action='store_true')
commandGroup.add_argument('--restart', help='Stop and start daemon', action='store_true')

args = parser.parse_args()
# endregion

daemon = DockerSpectatorDaemon(config['daemon.pid'])

if args.start:
    daemon.start()
elif args.stop:
    daemon.stop()
elif args.restart:
    daemon.restart()
else:
    pass
