#!/usr/bin/env python

import sys
import re
import commands
from config import config

container_name, field = re.findall('docker_containers_(.+)_(cpu|mem|net)$', sys.argv[0])[0]

if len(sys.argv) > 1 and sys.argv[1] == 'config':
    print('graph_category docker_containers')
    if field == 'cpu' or field == 'mem':
        print('graph_title {0} usage for container {1}'.format(field, container_name))
        print('graph_vlabel {0}'.format(field))
        print('{0}.label {0}'.format(field))
    elif field == 'net':
        print('graph_title Network usage for container {0}'.format(container_name))
        print('graph_order down up')
        print('graph_args --base 1000')
        print('graph_vlabel bits in (-) / out (+) per ${graph_period}')
        print('down.label received')
        print('down.type COUNTER')
        print('down.graph no')
        print('down.cdef down,8,*')
        print('up.label bps')
        print('up.type COUNTER')
        print('up.negative down')
        print('up.cdef up,8,*')
    else:
        pass
    sys.exit(0)

if field == 'cpu' or field == 'mem':
    print('{1}.value {0}'.format(commands.getoutput(
        '/usr/bin/env python {0} --average=5 --field={1} --container-name={2}'.format(
            config['docker.spectator'], field, container_name
        )
    ), field))
elif field == 'net':
    down, up = (commands.getoutput(
        '/usr/bin/env python {0} --average=5 --field={1} --container-name={2}'.format(
            config['docker.spectator'], field, container_name
        )
    )).split()
    print('down.label {0}'.format(down))
    print('up.label {0}'.format(up))
else:
    pass