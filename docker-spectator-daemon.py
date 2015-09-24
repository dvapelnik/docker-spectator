#!/usr/bin/env python

import logging
from argparse import ArgumentParser

from libs.classes.DockerSpeactatorDaemon import DockerSpectatorDaemon
from config import config


# region Arguments parsing
parser = ArgumentParser()

commonGroup = parser.add_argument_group('Common')
commonGroup.add_argument('-l', '--log-level',
                         help='Define log level',
                         choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                         default='WARNING')

commandGroup = parser.add_mutually_exclusive_group()
commandGroup.add_argument('--start', help='Start daemon', action='store_true')
commandGroup.add_argument('--stop', help='Stop daemon', action='store_true')
commandGroup.add_argument('--restart', help='Stop and start daemon', action='store_true')

args = parser.parse_args()
# endregion

logging.basicConfig(
    filename=config['daemon.log'],
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=getattr(logging, args.log_level.upper()))

daemon = DockerSpectatorDaemon(config['daemon.pid'])
daemon.set_logger(logging)

if args.start:
    logging.info('Starting daemon')
    daemon.start()
    logging.info('Daemon started')
elif args.stop:
    logging.info('Stopping daemon')
    daemon.stop()
    logging.info('Daemon stopped')
elif args.restart:
    logging.info('Restarting daemon')
    daemon.restart()
    logging.info('Daemon restarted')
else:
    pass
