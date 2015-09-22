#!/usr/bin/env python

import os.path, pickle
import libs.helpers as helpers


class DB:
    """DB Class"""

    def __init__(self, dbPath):
        self.dbPath = dbPath

    def getDbPath(self):
        return self.dbPath

    def readDbData(self, limitSeconds):
        if os.path.exists(self.dbPath):
            data = pickle.load(open(self.dbPath, 'rb'))
        else:
            data = {}

        return helpers.trimData(data, limitSeconds)

    def writeDbData(self, data, limitSeconds):
        pickle.dump(helpers.trimData(data, limitSeconds), open(self.dbPath, 'wb'))