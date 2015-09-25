#!/usr/bin/env python

import os.path
import pickle

import libs.helpers as helpers


class DB:
    """DB Class"""

    def __init__(self, dbPath):
        self.dbPath = dbPath

    def setLogger(self, logging):
        self.logging = logging

    def getDbPath(self):
        return self.dbPath

    def readDbData(self, limitSeconds):
        data = {}

        if os.path.exists(self.dbPath):
            try:
                db_read_file_descriptor = open(self.dbPath, 'rb')
                data = pickle.load(db_read_file_descriptor)
                db_read_file_descriptor.close()
            except BaseException:
                if self.logging:
                    self.logging.error(BaseException.message)

        return helpers.trimData(data, limitSeconds)

    def writeDbData(self, data, limitSeconds):
        db_write_file_descriptor = open(self.dbPath, 'wb')
        pickle.dump(helpers.trimData(data, limitSeconds), db_write_file_descriptor)
        db_write_file_descriptor.close()