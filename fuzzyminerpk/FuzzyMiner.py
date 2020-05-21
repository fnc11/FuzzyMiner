import Levenshtein

from fuzzyminerpk.ClusterUtil import ClusterUtil
from fuzzyminerpk.FMRepository import DataRepository, FilteredDataRepository
from fuzzyminerpk.Utility import FMLogUtils, cal_proximity, cal_endpoint, cal_originator, cal_datatype, cal_datavalue, \
    is_valid_matrix1D, is_valid_matrix2D


class Graph:
    def __init__(self, log, default_config):
        self.final_nodes = list()
        self.final_edges = list()
        self.config = default_config
        self.fm_log_util = FMLogUtils(log)
        self.cluster_util = ClusterUtil()
        self.log = log
        self.nodes = self.fm_log_util.nodes
        self.num_of_nodes = self.fm_log_util.num_of_nodes
        self.node_indices = self.fm_log_util.node_indices
        # extract data from logs
        self.data_repository = DataRepository(self.log, self.config)
        self.change_config(self.config)
        # apply filters on the data
        self.filtered_data_repository = FilteredDataRepository(self.log, self.data_repository, self.config.filter_config)
        self.apply_filters()
        self.cluster_util.clusterize(self.config.filter_config.node_filter, self.fm_log_util,self.data_repository, self.filtered_data_repository)

        # debug block start
        print("Nodes\n")
        for node in self.cluster_util.fm_nodes:
            print(node)
            print()

        print("\nClusters\n")
        for cluster in self.cluster_util.fm_clusters:
            print(cluster)
            print()

        print("\nEdges\n")
        for edge in self.cluster_util.fm_edges:
            print(edge)
            print()






    """
    This method is to be called when entire config object is changed, for e.g. during the initiation phase
    or when user chages config in the interface
    """

    def change_config(self, config):
        self.config = config
        self.data_repository.config = config
        self.data_repository.init_lists()
        self.data_repository.extract_primary_metrics()
        self.data_repository.normalize_primary_metrics()
        self.data_repository.extract_simple_aggregates()
        self.data_repository.extract_derivative_metrics()
        self.data_repository.normalize_derivative_metrics()
        # Final weighted values
        self.data_repository.extract_weighted_metrics()

        # Just for debug purpose
        # Debug block starts
        self.data_repository.debug_print_primary_metric_values()
        self.data_repository.debug_print_aggregate_values()
        self.data_repository.debug_print_derivative_metric_values()
        self.data_repository.debug_print_weighted_values()
        # Debug block ends

    """
    This methods if for first time when we initialize the graph, to apply filters with default values
    """

    def apply_filters(self):
        self.apply_concurrency_filter(self.config.filter_config.concurrency_filter)
        # in each method we first initialize corresponding lists to default values depending upon the context
        # no need to call node and edge filters separately as they will be applied in succession

        # Just for debug purpose
        # Debug block starts
        self.filtered_data_repository.debug_concurrency_filter_values()
        self.filtered_data_repository.debug_edge_filter_values()
        self.filtered_data_repository.debug_node_filter_values()
        # Debug block ends

    """
    For applying concurrency filter, can be called directly from front end when user changes value in
    concurrency filter, due to order, it'll call edge filter inherently
    """

    def apply_concurrency_filter(self, concurrency_filter):
        self.config.filter_config.concurrency_filter = concurrency_filter
        self.filtered_data_repository.apply_concurrency_filter(concurrency_filter)

    """
    For applying edge filter, can be called directly from front end when user changes value in
    edge filter, due to order, it'll call node filter inherently
    """

    def apply_edge_filter(self, edge_filter):
        self.config.filter_config.edge_filter = edge_filter
        self.filtered_data_repository.apply_edge_filter(edge_filter)

    """
    For applying node filter, can be called directly from front end when user changes value in
    node filter
    """

    def apply_node_filter(self, node_filter):
        self.config.filter_config.node_filter = node_filter
        self.filtered_data_repository.apply_node_filter(node_filter)