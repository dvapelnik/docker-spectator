#!/usr/bin/env python

import os

config = {
    'db.filename': os.path.dirname(os.path.abspath(__file__)) + '/' + 'db.bin',
    'db.limit.hours': 24,
    'docker.spectator': os.path.dirname(os.path.abspath(__file__)) + '/' + 'docker-spectator.py',
    'daemon.pid': '/var/run/docker-spectator-daemon.pid',
    'daemon.log': '/var/log/docker-spectator-daemon.log',
    'daemin.sleep': 10,
}