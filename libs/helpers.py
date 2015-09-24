#!/usr/bin/env python

import time


def cleanHumanBytes(s):
    _split = s.split(' ')
    _value = _split[0]
    _unit = _split[1]

    if len(_unit) > 1:
        _unit = _unit[0]

    return _value + _unit


def trimData(data, seconds, now=(int)(time.time())):
    return dict((k, v) for (k, v) in data.iteritems() if k > (now - seconds)) if len(data) else dict()


def hoursToSeconds(hours):
    return hours * 60 * 60


def minuteToSeconds(minutes):
    return (int)(minutes) * 60


def dump(data):
    print(data)
    return 0