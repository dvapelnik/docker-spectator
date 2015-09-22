#!/usr/bin/env python

import os


config = {
    'db.filename': os.path.dirname(os.path.abspath(__file__)) + '/' + 'db.bin',
    'db.limit.hours': 24,
}