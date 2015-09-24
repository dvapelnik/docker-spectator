# Munin plugin for monitoring docker containers

Plugin system consists of

1. `docker-spectator-daemon.py` periodic collecting data from `docker stats`
2. `docler-spectator.py` for collecting data, retrieve average data and list of containers with collected data
3. `docker_containers.py` munin plugin

## Requirements

1. Python 2.6+
2. `argparse` (`pip install argparse`)


## How to use munin plugin

### Download

```bash
cd /path/to/project/location # eg. `/root/scripts` or some another
# clone repo
git clone https://github.com/dvapelnik/docker-spectator
```

### Start daemon

```bash
cd docker-spectator
# start daemon
python docker-spectator-daemon.py --start
# wait some time for data collecting
```

### Make plugin symlinks

```bash
cd /etc/munin/plugin-conf.d
cp /path/to/project/location/docker-spectator/templates/plugin-conf.d/docker_containers_ .
cd ../plugins
# for monitoring single container
# replace [container_name] with container's name for monitoring
# replace [field_name] with field name for monitoring one of `cpu`, `mem` or `net`
ls -s /path/to/project/location/docker-spectator/docker_containers.py docker_containers_[container_name]_[field_name]
# for batch monitoring all containers
ls -s /path/to/project/location/docker-spectator/docker_containers.py docker_containers_[field_name]
```

> **Warning!** Batch graph monitoring available only for `cpu` and `mem` fields not for `network`

### Restart `munin-node`

```bash
service munin-node restart
```

### Make init.d file

```bash
cd /path/to/project/location/docker-spectator
cp templates/init.d/docker-spectatord /etc/init.d/
chmod +x /etc/init.d/docker-spectatord
```
> **Attention!** You should change daemon directory (`DAEMON_PATH`) in `/etc/init.d/docker-spectatord` to `/path/to/project/location/docker-spectator`

After this you can use init.d script for start/stop daemon which collects data from docker containers like this:
```bash
service docker-spectatord restart
```
or
```bash
/etc/init.d/docker-spectatord restart
```

## How to use `docker-spectator.py` only

`docker-spectator-daemon.py` is the daemon which exec `docker-spectator.py` every 10 seconds
This value is changeable. Look at `config/config.py`

Look at `--help` firstly:
```bash
python docker-spectator.py --help
```
```bash
usage: docker-spectator.py [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-cl]
                           [-a {5,10,15}] [-f {cpu,mem,net}]
                           [-cid CONTAINER_ID] [-cn CONTAINER_NAME] [-cids]

optional arguments:
  -h, --help            show this help message and exit

Common:
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Define log level

Collecting data:
  -cl, --collect        Should collect current data?

Retrieving average data:
  -a {5,10,15}, --average {5,10,15}
                        Specify time period in minutes for retrieve average
                        data
  -f {cpu,mem,net}, --field {cpu,mem,net}
                        Specify data field
  -cid CONTAINER_ID, --container-id CONTAINER_ID
                        Specify docker container id. Container id is preferred
                        if specified both
  -cn CONTAINER_NAME, --container-name CONTAINER_NAME
                        Specify docker container name. Container id is
                        preferred if specified both

Container:
  -cids, --container-ids
                        Retrieve container ids
```

You can use `docker-spectator.py` for retrieve list of containers which data already collected
```bash
python docker-spectator.py --container-ids
```
```
fa0a12244b9f fancy_bebe
6e1a5f381010 little_penguin
```

You can get collect data from active containers 
```bash
python docker-spectator.py --collect
```

You can retrieve average collected data for container by 5, 10, 15 minutes and specify container by name or id
Retrieve cpu average value by 5 minutes container specified by id:
```bash
python docker-spectator.py --average 5 --field=cpu --container-id=fa0a12244b9f
```
```
0.17
```
Retrieve cpu average value by 10 minutes container specified by name:
```bash
python docker-spectator.py --average 10 --field=mem --container-name=little_penguin
```
```
55344679
```
Or network. First part of result is downloaded traffic and second is uploaded. Values separated with *single* space
```bash
python docker-spectator.py --average 10 --field=net --container-name=little_penguin
```
```
738 55644 
```

## ToDo

1. In this moment network graph is not stable