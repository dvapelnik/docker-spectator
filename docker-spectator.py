#!/usr/bin/env python

from config import config
import sys
import time
import libs.helpers as helpers
from libs.classes.docker import Docker
from libs.classes.db import DB
from libs.classes.Data import Data
import argparse
import pprint

pp = pprint.PrettyPrinter(indent=4)

# region Arguments parsing
parser = argparse.ArgumentParser()

collectGroup = parser.add_argument_group('Collecting data')
collectGroup.add_argument('-cl', '--collect',
                          help='Should collect current data?',
                          action='store_true')

averageGroup = parser.add_argument_group('Retrieving average data')
averageGroup.add_argument('-a', '--average',
                          type=int,
                          choices=[5, 10, 15],
                          help='Specify time period in minutes for retrieve average data')
averageGroup.add_argument('-f', '--field',
                          choices=['cpu', 'mem', 'net'],
                          help='Specify data field')
averageGroup.add_argument('-cid', '--container-id',
                          help='Specify docker container id. Container id is preferred if specified both')
averageGroup.add_argument('-cn', '--container-name',
                          help='Specify docker container name. Container id is preferred if specified both')

args = parser.parse_args()

# print(args)
# endregion

db = DB(config['db.filename'])
docker = Docker()

if args.collect:
    secondsLimit = helpers.hoursToSeconds(config['db.limit.hours'])
    _data = db.readDbData(secondsLimit)
    _data[int(time.time())] = docker.getStatsDataArray()
    db.writeDbData(_data, secondsLimit)

if args.average:
    if not args.field:
        print('Error: field type not specified')
        parser.print_help()
        sys.exit(1)

    secondsAverage = helpers.minuteToSeconds(args.average)

    dataWorker = Data(db.readDbData(secondsAverage))

    if args.field == 'cpu':
        result = dataWorker.getCpuData(container_id=args.container_id, container_name=args.container_name)
    elif args.field == 'mem':
        result = dataWorker.getMemPercent(container_id=args.container_id, container_name=args.container_name)
    else:
        resultInput = dataWorker.getNetTotalInputTraffic(
            container_id=args.container_id, container_name=args.container_name)
        resultOutput = dataWorker.getNetTotalOutputTraffic(
            container_id=args.container_id, container_name=args.container_name)

        result = [resultInput, resultOutput]
    print(result)


