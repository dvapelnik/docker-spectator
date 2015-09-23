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

print(args)
# endregion

db = _db.DB(config.config['db.filename'])
docker = _docker.Docker()

if args.collect:
    secondsLimit = helpers.hoursToSeconds(config.config['db.limit.hours'])
    _data = db.readDbData(secondsLimit)
    _data[int(time.time())] = docker.getStatsDataArray()
    db.writeDbData(_data, secondsLimit)

if args.average:
    if not args.field:
        print('Error: field type not specified')
        parser.print_help()
        sys.exit(1)

    secondsAverage = helpers.minuteToSeconds(args.average)

    _data = db.readDbData(secondsAverage)
    # pp.pprint(_data)

    _filteredData = _data

    if args.container_name:
        _filteredData = {
            ts: {container_id: data for (container_id, data) in containers.iteritems()
                 if data['name'] == args.container_name} for (ts, containers) in _data.iteritems()}

    if args.container_id:
        _filteredData = {
            ts: {container_id: data for (container_id, data) in containers.iteritems()
                 if container_id == args.container_id} for (ts, containers) in _data.iteritems()}

    pp.pprint(_filteredData)

    if args.field == 'cpu':
        print('cpu')
    elif args.field == 'mem':
        print('mem')
    else:
        print('net')



# if sys.argv[1].startswith('--average', 0, 9):
# _interval = sys.argv[1].split('=')[1]
# _intervalSeconds = helpers.minuteToSeconds(_interval)
# _data = db.readDbData(_intervalSeconds)
#
# print(_data)



