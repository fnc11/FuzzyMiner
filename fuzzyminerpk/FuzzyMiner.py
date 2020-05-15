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
        self.num_of_nodes = len(self.nodes)
        self.node_indices = dict()
        self.update_node_index()
        # extract data from logs
        self.change_config(self.config)

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
        # there will be a cluster objects list also after node filtering basically after clusterization proces

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
    This method is to be called when entire config object is changed, for e.g. during the initiation phase
    or when user chages config in the interface
    """
    def change_config(self, config):
        self.config = config
        self.data_repository = DataRepository(self.log, self.config)
        self.data_repository.init_lists()
        self.data_repository.extract_primary_metrics()
        self.data_repository.normalize_primary_metrics()
        self.data_repository.extract_simple_aggregates()
        self.data_repository.extract_derivative_metrics()
        self.data_repository.normalize_derivative_metrics()
        # Final weighted values
        self.data_repository.extract_weighted_metrics()

        # Just for debug purpose
        self.data_repository.debug_print_primary_metric_values()
        self.data_repository.debug_print_aggregate_values()
        self.data_repository.debug_print_derivative_metric_values()
        self.data_repository.debug_print_weighted_values()

    def update_node_index(self):
        idx = 0
        for node in self.nodes:
            self.node_indices[node] = idx
            idx += 1


class Cluster:
    pass
