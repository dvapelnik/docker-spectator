#!/usr/bin/env python

import commands
import time
from config import config
from libs.classes.daemon import Daemon


class DockerSpectatorDaemon(Daemon):
    def run(self):
        while True:
            print('/usr/bin/env python {0} {1}'.format(config['docker.spectator'], '--collect'))
            # commands.getstatusoutput(
            #     '/usr/bin/env python {0} {1}'.format(config['docker.spectator'], '--collect'))
            time.sleep(config['daemin.sleep'])
