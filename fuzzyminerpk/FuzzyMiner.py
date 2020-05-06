class Graph:
    def __init__(self, log, default_config):
        self.config = default_config
        self.log = log
        self.nodes_dict = dict()
        self.edges_dict = dict()
        self.extract_dicts()
        self.clusters = list()
        self.apply_config()

    def extract_dicts(self):
        for trace in self.log:
            num = len(trace)
            for i in range(0, num):
                # calculating nodes dictionary
                if trace[i]['concept:name'] in self.nodes_dict.keys():
                    self.nodes_dict[trace[i]['concept:name']] += 1
                else:
                    self.nodes_dict[trace[i]['concept:name']] = 1
                # calculating edges dictionary
                if num > 1 and i > 0:
                    if trace[i - 1]['concept:name'] + "->" + trace[i]['concept:name'] in self.edges_dict.keys():
                        self.edges_dict[trace[i - 1]['concept:name'] + "->" + trace[i]['concept:name']] += 1
                    else:
                        self.edges_dict[trace[i - 1]['concept:name'] + "->" + trace[i]['concept:name']] = 1

    def change_config(self, new_config):
        pass

    def apply_config(self):
        pass


class Cluster:
    pass
