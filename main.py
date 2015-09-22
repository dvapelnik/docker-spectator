#!/usr/bin/env python

import config
import sys
import time
import libs.helpers as helpers
import libs.classes.docker as _docker
import libs.classes.db as _db
import argparse
import pprint

pp = pprint.PrettyPrinter(indent=4)

# region Arguments parsing
parser = argparse.ArgumentParser()

parser.add_argument('-c', '--collect',
                    help='Should collect current data?',
                    action='store_true')
parser.add_argument('-co', '--collect-only',
                    help='Should only collect data',
                    action='store_true')
parser.add_argument('-a', '--average',
                    type=int,
                    choices=[5, 10, 15],
                    default=5,
                    help='Specify time period in minutes for retrieve average data')
parser.add_argument('-f', '--field',
                    choices=['cpu', 'mem', 'net'],
                    help='Specify data field')
args = parser.parse_args()

print(args)
# endregion

sys.exit(0)

if not args.field:
    print('--field argument is required')
    sys.exit(1)

db = _db.DB(config.config['db.filename'])
docker = _docker.Docker()

if args.collect:
    secondsLimit = helpers.hoursToSeconds(config.config['db.limit.hours'])

    _data = db.readDbData(secondsLimit)

    _data[int(time.time())] = docker.getStatsDataArray()
    db.writeDbData(_data, secondsLimit)

if sys.argv[1].startswith('--average', 0, 9):
    _interval = sys.argv[1].split('=')[1]

    _intervalSeconds = helpers.minuteToSeconds(_interval)

    _data = db.readDbData(_intervalSeconds)

    print(_data)


else:
    sys.exit(1)



