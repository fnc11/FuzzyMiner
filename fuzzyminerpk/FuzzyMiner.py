class Graph:
    def __init__(self, log, default_config):
        self.config = default_config
        self.log = log
        self.nodes_dict = dict()
        self.nodes_index = dict()
        # Warning only 20 activities is considered at max
        self.edges_list = [[0 for x in range(20)] for y in range(20)]
        self.edge_distance_values = [[0 for x in range(20)] for y in range(20)]
        self.extract_dicts()

        # Metrics Operations
        # unary
        self.node_routing_values = dict()
        self.unary_sig_values = dict()
        self.cal_unary_metrics()
        # binary
        self.edge_distance_values = list()
        self.binary_sig_values = list()
        self.cal_binary_metrics()
        # binary correlation
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
                    self.edges_list[self.nodes_index[trace[i - 1]['concept:name']]][
                        self.nodes_index[trace[i]['concept:name']]] += 1

    def change_config(self, new_config):
        pass

    def apply_config(self):
        pass

    def cal_unary_metrics(self):
        in_arcs = 0
        out_arcs = 0
        self.extract_dicts()
        for row in range(len(self.edges_list)):
            for col in range(len(self.edges_list[row])):
                out_arcs += self.edges_list[row][col]
                in_arcs += self.edges_list[col][row]
                self.node_routing_values[row][col] = abs(in_arcs - out_arcs)

        # Hard-coding the weights
        node_sig_weights_freq = 0.5
        node_sig_weights_routing = 0.5

        # Finding the aggregate unary node significance
        for key in self.nodes_dict:
            if key in self.node_routing_values:
                self.unary_sig_values[key] = (self.nodes_dict[key] * node_sig_weights_freq) + (self.node_routing_values[key] * node_sig_weights_routing)
            else:
                pass

    def cal_binary_metrics(self):
        self.extract_dicts()
        for row in range(len(self.edges_list)):
            for col in range(len(self.edges_list[row])):
                a = self.edges_list[row][col]
                n1 = self.nodes_dict[row]
                n2 = self.nodes_dict[col]
                self.edge_distance_values = abs((n1 + n2) - a)

        # Hard-coding the weights
        edge_sig_weights_freq = 0.5
        edge_sig_weights_dist = 0.5

        # Finding the aggregate binary edge significance
        for key in self.nodes_dict:
            if key in self.edge_distance_values:
                self.unary_sig_values[key] = (self.nodes_dict[key] * edge_sig_weights_freq) + (self.edge_distance_values * edge_sig_weights_dist)
            else:
                pass

        return self.unary_sig_values

    def cal_binary_corr_metrics(self):
        pass


class Cluster:
    pass
