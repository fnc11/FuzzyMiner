class Graph:
    def __init__(self, log, default_config):
        self.config = default_config
        self.log = log
        self.nodes_dict = dict()
        self.nodes_index = dict()
        # Warning only 20 activities is considered at max
        self.edges_list = [[0 for x in range(10)] for y in range(10)]
        self.extract_dicts()

        # Metrics Operations
        #uniary
        self.node_routing_values = dict()
        self.unary_sig_values = dict()
        self.cal_uniary_metrics()
        #binary
        self.edge_distance_values = list()
        self.binary_sig_values = list()
        self.cal_binary_metrics()
        #binary correlation
        self.time_diff_values = list()
        self.resource_corr_values = list()
        self.activity_corr_values = list()
        self.cal_binary_corr_metrics()


        self.clusters = list()
        self.apply_config()

    def extract_dicts(self):
        idx = 0
        for trace in self.log:
            num = len(trace)
            for i in range(0, num):
                # calculating nodes dictionary
                if trace[i]['concept:name'] in self.nodes_dict.keys():
                    self.nodes_dict[trace[i]['concept:name']] += 1
                else:
                    self.nodes_index[trace[i]['concept:name']] = idx
                    self.nodes_dict[trace[i]['concept:name']] = 1
                    idx += 1
                #     Add some kind of notifier to the user if activities exceed max num(20 for eg)
                # calculating edges 2D matrix
                if num > 1 and i > 0:
                    self.edges_list[self.nodes_index[trace[i - 1]['concept:name']]][self.nodes_index[trace[i]['concept:name']]] += 1

    def change_config(self, new_config):
        pass

    def apply_config(self):
        pass


class Cluster:
    pass
