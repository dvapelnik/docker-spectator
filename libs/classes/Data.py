#!/usr/bin/env python

from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)


class Data:
    def __init__(self, dataArray):
        self.dataArray = dataArray

    def __filterDataByContainerName(self, container_name):
        return {ts: {container_id: data for (container_id, data) in containers.iteritems()
                     if data['name'] == container_name} for (ts, containers) in self.dataArray.iteritems()}

    def __filterDataByContainerId(self, container_id):
        return {ts: {_container_id: data for (_container_id, data) in containers.iteritems()
                     if _container_id == container_id} for (ts, containers) in self.dataArray.iteritems()}

    def __getProcessData(self, container_id=None, container_name=None):
        if not container_id and not container_name:
            raise Exception('One of container_id or container_name should be defined')

        if container_name:
            process_data = self.__filterDataByContainerName(container_name)

        if container_id:
            process_data = self.__filterDataByContainerId(container_id)

        return process_data

    def getContainerIds(self):
        ids_dict = {}

        for ts, containersData in self.dataArray.iteritems():
            for containerId, data in containersData.iteritems():
                ids_dict[containerId] = None

        return ids_dict.keys()

    def getContainerNameById(self, container_id):
        return self.__filterDataByContainerId(container_id) \
            .itervalues().next() \
            .itervalues().next()['name']

    def getCpuData(self, container_id=None, container_name=None):

        process_data = self.__getProcessData(container_id=container_id, container_name=container_name)

        reduced_cpu = 0
        for ts, containerData in process_data.iteritems():
            for _container_id, _container_data in containerData.iteritems():
                reduced_cpu += (float)(_container_data['cpu'])

        return round(reduced_cpu / len(process_data), 2)

    def getMemPercent(self, container_id=None, container_name=None):
        process_data = self.__getProcessData(container_id=container_id, container_name=container_name)

        reduced_mem_percent = 0
        for ts, containerData in process_data.iteritems():
            for _container_id, _container_data in containerData.iteritems():
                reduced_mem_percent += (float)(_container_data['mem']['percent'])

        return round(reduced_mem_percent / len(process_data), 2)

    def __getNetTotalTraffic(self, direction, container_id=None, container_name=None):
        process_data = self.__getProcessData(container_id=container_id, container_name=container_name)

        return process_data.get(process_data.keys()[-1]).itervalues().next()['network'][direction] - \
               process_data.get(process_data.keys()[0]).itervalues().next()['network'][direction]

    def getNetTotalInputTraffic(self, container_id=None, container_name=None):
        return self.__getNetTotalTraffic(direction='i',
                                         container_id=container_id, container_name=container_name)

    def getNetTotalOutputTraffic(self, container_id=None, container_name=None):
        return self.__getNetTotalTraffic(direction='o',
                                         container_id=container_id, container_name=container_name)
