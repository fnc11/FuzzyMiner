import Levenshtein


class Graph:
    def __init__(self, log, default_config):
        self.config = default_config
        self.log = log
        self.nodes_dict = dict()
        self.nodes_index = dict()
        # Warning only 20 activities is considered at max
        self.edges_list = [[0 for x in range(20)] for y in range(20)]
        self.extract_dicts()

        # data to show on the canvas
        # intermediate data after applying concurrency filter
        self.nodes_dict_aft_conc_filter = dict()  # not sure if this is needed, but can decide later
        self.edges_sig_aft_conc_filter = [[0 for x in range(20)] for y in range(20)]
        self.edges_corr_aft_conc_filter = [[0 for x in range(20)] for y in range(20)]
        # intermediate data after applying edge filter
        self.nodes_dict_aft_edge_filter = dict()  # not sure if this is needed, but can decide later
        self.edges_sig_aft_edge_filter = [[0 for x in range(20)] for y in range(20)]
        self.edges_corr_aft_edge_filter = [[0 for x in range(20)] for y in range(20)]
        # final data after applying all/node filter
        self.nodes_dict_aft_node_filter = dict()
        self.edges_sig_aft_node_filter = [[0 for x in range(20)] for y in range(20)]
        self.edges_corr_aft_node_filter = [[0 for x in range(20)] for y in range(20)]
        # there will be a cluster objects list also after node filtering basically after clusterization process

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
        self.time_diff_values = [[0 for x in range(20)] for y in range(20)]
        # initializing with 1 as max disimlar value
        self.resource_corr_values = [[1 for x in range(20)] for y in range(20)]
        self.activity_corr_values = [[1 for x in range(20)] for y in range(20)]
        self.binary_corr_sig_values = [[0 for x in range(20)] for y in range(20)]
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

    def cal_unary_metrics(self):
        in_arcs = 0
        out_arcs = 0
        self.extract_dicts()
        for row in range(len(self.edges_list)):
            for col in range(len(self.edges_list[row])):
                out_arcs += self.edges_list[row][col]
                in_arcs += self.edges_list[col][row]
                self.node_routing_values[row][col] = abs(in_arcs - out_arcs)

    def cal_binary_metrics(self):
        self.extract_dicts()
        for row in range(len(self.edges_list)):
            for col in range(len(self.edges_list[row])):
                a = self.edges_list[row][col]
                n1 = self.nodes_dict[row]
                n2 = self.nodes_dict[col]
                self.edge_distance_values = abs((n1 + n2) - a)

    def cal_binary_corr_metrics(self):
        for trace in self.log:
            num = len(trace)
            for i in range(0, num):
                if i > 0:
                    event = trace[i]
                    prev_event = trace[i - 1]
                    self.time_diff_values[self.nodes_index[prev_event['concept:name']]][
                        self.nodes_index[event['concept:name']]] = \
                        event['time:timestamp'] - prev_event['time:timestamp']
                    # since all logs don't have resources
                    if 'org:resource' in event and 'org:resource' in prev_event:
                        self.resource_corr_values[self.nodes_index[prev_event['concept:name']]][
                            self.nodes_index[event['concept:name']]] = \
                            Levenshtein.ratio(event['org:resource'], prev_event['org:resource'])
                    self.activity_corr_values[self.nodes_index[prev_event['concept:name']]][
                        self.nodes_index[event['concept:name']]] = \
                        Levenshtein.ratio(event['concept:name'], prev_event['concept:name'])

    def update_unary_sig_values(self):
        # Hard-coding the weights
        node_sig_weights_freq = 0.5
        node_sig_weights_routing = 0.5

        # Finding the aggregate unary node significance
        for key in self.nodes_dict:
            if key in self.node_routing_values:
                self.unary_sig_values[key] = (self.nodes_dict[key] * node_sig_weights_freq) + (
                        self.node_routing_values[key] * node_sig_weights_routing)
            else:
                pass

    def update_binary_sig_values(self):
        # Hard-coding the weights
        edge_sig_weights_freq = 0.5
        edge_sig_weights_dist = 0.5

        # Finding the aggregate binary edge significance
        for key in self.nodes_dict:
            if key in self.edge_distance_values:
                self.unary_sig_values[key] = (self.nodes_dict[key] * edge_sig_weights_freq) + (
                        self.edge_distance_values * edge_sig_weights_dist)
            else:
                pass

    def update_binary_corr_sig_values(self):
        w1 = 0.5
        w2 = 0.5
        w3 = 0.5
        inc1 = True
        inc2 = True
        inc3 = True
        num = 0
        if inc1:
            num += 1
        if inc2:
            num += 1
        if inc3:
            num += 1
        if num != 0:  # avoids exception and no need to caluclate if no metric is selected
            for i in range(0, 20):
                for j in range(0, 20):
                    if inc1:
                        self.binary_corr_sig_values[i][j] += w1 * self.time_diff_values[i][j] / num
                    if inc2:
                        self.binary_corr_sig_values[i][j] += w2 * self.resource_corr_values[i][j] / num
                    if inc3:
                        self.binary_corr_sig_values[i][j] += w3 * self.activity_corr_values[i][j] / num

    """
    For applying concurrency filter, can be called directly from front end when user changes value in
    concurrency filter, due to order, it'll call edge inherently
    """

    def apply_concurrency_filter(self):
        # write code after that
        self.apply_edge_filter()
        pass

    """
    For applying edge filter, can be called directly from front end when user changes value in
    edge filter, due to order, it'll call node filter inherently
    """

    def apply_edge_filter(self):
        # write code after that
        self.apply_node_filter()
        pass

    """
    For applying node filter, can be called directly from front end when user changes value in
    node filter
    """

    def apply_node_filter(self):
        pass

    """
    To be called when only change is in the metric configs, and it'll call filter methods again
    """

    def change_metric_configs(self, new_metric_configs):
        # check here which of the metric configs are changed and call update method accordingly
        # for now we can call all the update methods, later we'll optimize
        self.update_unary_sig_values()
        self.update_binary_sig_values()
        self.update_binary_corr_sig_values()

        #  only call to this is enough, it'll call ege filter itself and edge will call node filter.
        self.apply_concurrency_filter()

    """
    This method is to be called when entire config object is changed, for e.g. during the initiation phase
    """

    def apply_config(self):
        self.update_unary_sig_values()
        self.update_binary_sig_values()
        self.update_binary_corr_sig_values()

        #  only call to this is enough, it'll call ege filter itself and edge will call node filter.
        self.apply_concurrency_filter()


class Cluster:
    pass
