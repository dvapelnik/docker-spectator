#!/usr/bin/env python

import os

root_path = os.path.dirname(os.path.abspath(__file__)) + '/'

config = {
    'db.filename': root_path + 'db.bin',
    'db.limit.hours': 1,
    'docker.spectator': root_path + 'docker-spectator.py',
    'docker.spectator.log': root_path + 'log/docker-spectator.log',
    'daemon.pid': root_path + 'run/docker-spectator-daemon.pid',
    'daemon.log': root_path + 'log/docker-spectator-daemon.log',
    'daemon.sleep': 10,
}