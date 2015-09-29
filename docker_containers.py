#!/usr/bin/env python

import sys
import re
import commands

from config import config


command_for_average_template = '/usr/bin/env python {0} --average=5 --field={1} --container-name={2}'
command_for_container_names_template = "/usr/bin/env python {0} --container-ids | cut -d' ' -f2"

batch_containers = re.findall('docker_containers_(cpu|mem|net)$', sys.argv[0])
single_container = re.findall('docker_containers_(.+)_(cpu|mem|net)$', sys.argv[0])

is_single_container = (bool)(single_container) and not (bool)(batch_containers)

if is_single_container:
    container_name, field = single_container[0]
else:
    field = batch_containers[0]
    container_names = commands.getoutput(command_for_container_names_template.format(config['docker.spectator'])).split(
        '\n')

if len(sys.argv) > 1 and sys.argv[1] == 'config':
    print('graph_category docker_containers')
    if field == 'cpu' or field == 'mem':
        if is_single_container:
            print('graph_title {0} usage for container {1}'.format(field, container_name))
            print('{0}.label {0}'.format(field))
        else:
            print('graph_title {0} usage for containers'.format(field))
            for container_name in container_names:
                print('{0}.label {0}'.format(container_name))

        print('graph_vlabel {0}'.format(field))
    elif field == 'mem':
        if is_single_container:
            print('graph_title {0} usage for container {1}'.format(field, container_name))
            print('{0}.label {0}'.format(field))
        else:
            print('graph_title {0} usage for containers'.format(field))
            for container_name in container_names:
                print('{0}.label {0}'.format(container_name))

        print('graph_vlabel {0}'.format(field))
        print('graph_args --base 1000')
    elif field == 'net' and is_single_container:
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
    if is_single_container:
        print('{1}.value {0}'.format(commands.getoutput(
            command_for_average_template.format(config['docker.spectator'], field, container_name)
        ), field))
    else:
        for container_name in container_names:
            print('{1}.value {0}'.format(commands.getoutput(
                command_for_average_template.format(config['docker.spectator'], field, container_name)
            ), container_name))
elif field == 'net' and is_single_container:
    down, up = (commands.getoutput(
        command_for_average_template.format(config['docker.spectator'], field, container_name)
    )).split()
    print('down.value {0}'.format(down))
    print('up.value {0}'.format(up))
else:
    pass