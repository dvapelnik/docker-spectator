#!/usr/bin/env python

import sys
import time
import libs.helpers as helpers
import logging
from config import config
from pprint import PrettyPrinter
from argparse import ArgumentParser
from libs.classes.docker import Docker
from libs.classes.db import DB
from libs.classes.Data import Data

pp = PrettyPrinter(indent=4)

# region Arguments parsing
parser = ArgumentParser()

commonGroup = parser.add_argument_group('Common')
commonGroup.add_argument('-l', '--log-level',
                         help='Define log level',
                         choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                         default='WARNING')

collectGroup = parser.add_argument_group('Collecting data')
collectGroup.add_argument('-cl', '--collect',
                          help='Should collect current data?',
                          action='store_true')

averageGroup = parser.add_argument_group('Retrieving average data')
averageGroup.add_argument('-a', '--average',
                          type=int,
                          choices=[5, 10, 15],
                          default=5,
                          help='Specify time period in minutes for retrieve average data')
averageGroup.add_argument('-f', '--field',
                          choices=['cpu', 'mem', 'net'],
                          help='Specify data field')
averageGroup.add_argument('-cid', '--container-id',
                          help='Specify docker container id. Container id is preferred if specified both')
averageGroup.add_argument('-cn', '--container-name',
                          help='Specify docker container name. Container id is preferred if specified both')

containerGroup = parser.add_argument_group('Container')
containerGroup.add_argument('-cids', '--container-ids',
                            help='Retrieve container ids',
                            action='store_true')

args = parser.parse_args()

# print(args)
# endregion

logging.basicConfig(
    filename=config['docker.spectator.log'],
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=getattr(logging, args.log_level.upper()))

db = DB(config['db.filename'])
docker = Docker()

if args.collect:
    logging.info('Collecting data from docker daemon')
    secondsLimit = helpers.hoursToSeconds(config['db.limit.hours'])
    _data = db.readDbData(secondsLimit)
    _data[int(time.time())] = docker.getStatsDataArray()
    db.writeDbData(_data, secondsLimit)
    logging.info('Data collected')

if args.container_ids or args.average:
    secondsAverage = helpers.minuteToSeconds(args.average)

    dataWorker = Data(db.readDbData(secondsAverage))

if args.container_ids:
    for container_id in dataWorker.getContainerIds():
        print('{0}  {1}'.format(container_id, dataWorker.getContainerNameById(container_id)))

if args.average and not args.container_ids:
    if not args.field:
        logging.error('Error: field type not specified')
        parser.print_help()
        sys.exit(1)

    if args.field == 'cpu':
        logging.info('Retrieving CPU% data')
        result = dataWorker.getCpuData(container_id=args.container_id, container_name=args.container_name)
    elif args.field == 'mem':
        logging.info('Retrieving MEM% data')
        result = dataWorker.getMemPercent(container_id=args.container_id, container_name=args.container_name)
    else:
        logging.info('Retrieving NETWORK traffic data')
        logging.info('Retrieving NETWORK input traffic data')
        resultInput = dataWorker.getNetTotalInputTraffic(
            container_id=args.container_id, container_name=args.container_name)
        logging.info('Retrieving NETWORK output traffic data')
        resultOutput = dataWorker.getNetTotalOutputTraffic(
            container_id=args.container_id, container_name=args.container_name)

        result = [resultInput, resultOutput]
    print(result)


