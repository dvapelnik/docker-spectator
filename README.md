# Munin plugin for monitoring docker containers

Plugin system consists of

1. `docker-spectator-daemon.py` periodic collecting data from `docker stats`
2. `docler-spectator.py` for collecting data, retrieve average data and list of containers with collected data
3. `docker_containers.py` munin plugin

## Requirements

1. Python 2.6+
2. `argparse` (`pip install argparse`)


## How to use

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
cd /etc/munin/templates/plugin-conf.d
cp /path/to/project/location/docker-spectator/plugin-conf.d/docker_containers_ .
cd ../plugins
# for monitoring single container
# replace [container_name] with container's name for monitoring
# replace [field_name] with field name for monitoring one of `cpu`, `mem` or `net`
ls -s /path/to/project/location/docker-spectator/docker_containers.py docker_containers_[container_name]_[field_name]
# for batch monitoring all containers
ls -s /path/to/project/location/docker-spectator/docker_containers.py docker_containers_[field_name]
```

> Warning! Batch graph monitoring available only for `cpu` and `mem` fields not for `network`

### Restart `munin-node`

```bash
service munin-node restart
```

## ToDo

1. In this moment network graph is not stable