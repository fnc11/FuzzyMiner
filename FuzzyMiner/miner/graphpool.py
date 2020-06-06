#!python3
# -*- coding=UTF-8 -*-

# Create by Eric Li at 27.05.20 for FuzzyMiner

import hashlib
import threading
from datetime import datetime, timedelta


class GraphPool(object):
    __max_size__ = 20
    __max_delta__ = timedelta(hours=2)
    _instance_lock = threading.Lock()
    __pool = {}

    def __init__(self):
        pass

    # singleton, make sure to get the only one object for graph pool
    def __new__(cls, *args, **kwargs):
        if not hasattr(GraphPool, "_instance"):
            with GraphPool._instance_lock:
                if not hasattr(GraphPool, "_instance"):
                    GraphPool._instance = object.__new__(cls)
        return GraphPool._instance

    def __generate_id(self, data):
        md5 = hashlib.md5()
        md5.update(data.encode('utf-8'))
        return md5.hexdigest()

    def __decrease_graph(self):
        delta = timedelta(seconds=0)
        for key in list(self.__pool.keys()):
            if self.__pool[key]["last_update"] >= self.__max_delta__:
                del self.__pool[key]
            else:
                temp = datetime.now() - self.__pool[key]["last_update"]
                if delta < temp:
                    delta = temp
                    item = key
        if len(self.__pool) >= self.__max_size__:
            del self.__pool[item]

    @staticmethod
    def __joint_ip_port(ip, port):
        return str(ip) + str(port)

    def update_graph(self, ip, port, graph):
        id = self.__generate_id(self.__joint_ip_port(ip, port))
        if id not in self.__pool.keys():
            if len(self.__pool) >= self.__max_size__:
                self.__decrease_graph()
            self.__pool[id] = {
                "graph": graph,
                "last_update": datetime.now()
            }
        else:
            self.__pool[id]["graph"] = graph
            self.__pool[id]["last_update"] = datetime.now()
        return id

    def get_graph(self, ip, port):
        return self.get_graph_by_id(self.__generate_id(self.__joint_ip_port(ip, port)))

    def get_graph_by_id(self, id):
        return self.__pool[id]["graph"]
