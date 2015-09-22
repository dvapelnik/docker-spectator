#!/usr/bin/env python

import commands
import re
import libs.helpers as helpers
import libs.bytes_converting as bytes_converting


class Docker:
    def getStatsDataArray(self):
        result = commands.getoutput(
            "docker ps | tail -n +2 | cut -d' ' -f1 | xargs docker stats --no-stream | tail -n +2"
        )

        print(result)

        resultDataArray = {}

        for line in result.split('\n'):
            _split = re.compile("\s{2,}").split(line)

            _humanMemBytes = _split[2].split('/')
            _humanNetworkBytes = _split[4].split('/')

            resultDataArray[_split[0]] = {
                'name': commands.getoutput("docker inspect --format='{{.Name}}' " + _split[0])[1:],
                'cpu': _split[1].replace('%', ''),
                'mem': {
                    'usage': bytes_converting.human2bytes(helpers.cleanHumanBytes(_humanMemBytes[0])),
                    'percent': _split[3].replace('%', ''),
                    'total': bytes_converting.human2bytes(helpers.cleanHumanBytes(_humanMemBytes[1])),
                },
                'network': {
                    'i': bytes_converting.human2bytes(helpers.cleanHumanBytes(_humanNetworkBytes[0])),
                    'o': bytes_converting.human2bytes(helpers.cleanHumanBytes(_humanNetworkBytes[1])),
                }
            }

        return resultDataArray