import Levenshtein

from fuzzyminerpk.FMRepository import DataRepository
from fuzzyminerpk.Utility import FMLogUtils, cal_proximity, cal_endpoint, cal_originator, cal_datatype, cal_datavalue, \
    is_valid_matrix1D, is_valid_matrix2D

class Graph:
    def __init__(self, log, default_config):
        self.config = default_config
        self.fm_log_util = FMLogUtils(log)
        self.log = log
        self.nodes = self.fm_log_util.get_event_classes()
        print(self.nodes)
        self.num_of_nodes = len(self.nodes)
        self.node_indices = dict()
        self.update_node_index()

        self.data_repository = DataRepository(log, default_config)
        self.data_repository.init_lists()
        self.data_repository.extract_primary_metrics()
        self.data_repository.normalize_primary_metrics()
        self.data_repository.extract_simple_aggregates()
        self.data_repository.extract_derivative_metrics()
        self.data_repository.normalize_derivative_metrics()

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

        self.clusters = list()
        self.apply_config()

    def update_unary_sig_values(self):
        # Hard-coding the weights
        node_sig_weights_freq = 0.5
        node_sig_weights_routing = 0.5

        # # Finding the aggregate unary node significance
        # for key in self.nodes_dict:
        #     if key in self.node_routing_values:
        #         self.unary_sig_values[key] = (self.nodes_dict[key] * node_sig_weights_freq) + (
        #                 self.node_routing_values[key] * node_sig_weights_routing)
        #     else:
        #         pass
        pass

    def update_binary_sig_values(self):
        # Hard-coding the weights
        edge_sig_weights_freq = 0.5
        edge_sig_weights_dist = 0.5

        # # Finding the aggregate binary edge significance
        # for key in self.nodes_dict:
        #     if key in self.edge_distance_values:
        #         self.unary_sig_values[key] = (self.nodes_dict[key] * edge_sig_weights_freq) + (
        #                 self.edge_distance_values * edge_sig_weights_dist)
        #     else:
        #         pass
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

    def update_node_index(self):
        idx = 0
        for node in self.nodes:
            self.node_indices[node] = idx
            idx += 1


class Cluster:
    pass
