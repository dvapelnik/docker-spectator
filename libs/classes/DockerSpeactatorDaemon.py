#!/usr/bin/env python

import commands
import time
from config import config
from libs.classes.daemon import Daemon


class DockerSpectatorDaemon(Daemon):
    def set_logger(self, logger):
        self.logger = logger

    def run(self):
        while True:
            self.__log('INFO', 'Running')
            commands.getstatusoutput(
                '/usr/bin/env python {0} {1}'.format(config['docker.spectator'], '--collect'))
            time.sleep(config['daemon.sleep'])

    def __log(self, level, message):
        if self.logger:
            log_method = getattr(self.logger, level.lower())
            log_method(message)
