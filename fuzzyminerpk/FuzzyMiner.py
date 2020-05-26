import Levenshtein

from fuzzyminerpk.ClusterUtil import ClusterUtil
from fuzzyminerpk.FMRepository import DataRepository, FilteredDataRepository
from fuzzyminerpk.Utility import FMLogUtils
from datetime import datetime


class Graph:
    def __init__(self, log):
        self.config = None
        self.fm_log_util = FMLogUtils(log)
        self.cluster_util = ClusterUtil()
        self.log = log
        self.data_repository = DataRepository(self.log)
        self.filtered_data_repository = FilteredDataRepository(self.log)
        self.fm_nodes = None
        self.fm_clusters = None
        self.fm_edges = None


    """
    This method is to be called when entire config object is changed, for e.g. during the initiation phase
    or when user changes config in the interface
    """

    def apply_config(self, config):
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

        # apply filters on the data
        self.apply_filters()

        # Just for debug purpose
        # Debug block starts
        print("Nodes\n")
        for node in self.filtered_data_repository.cluster_util.fm_nodes:
            print(node)
            print()

        print("\nClusters\n")
        for cluster in self.filtered_data_repository.cluster_util.fm_clusters:
            print(cluster)
            print()

        print("\nEdges\n")
        for edge in self.filtered_data_repository.cluster_util.fm_edges:
            print(edge)
            print()

        # self.data_repository.debug_print_primary_metric_values()
        # self.data_repository.debug_print_aggregate_values()
        # self.data_repository.debug_print_derivative_metric_values()
        # self.data_repository.debug_print_weighted_values()
        # Debug block ends

    """
    This methods is for first time when we initialize the graph, to apply filters with default values
    """

    def apply_filters(self):
        self.filtered_data_repository.filter_config = self.config.filter_config
        self.filtered_data_repository.data_repository = self.data_repository
        self.apply_concurrency_filter(self.config.filter_config.concurrency_filter)

        # Just for debug purpose
        # Debug block starts
        # self.filtered_data_repository.debug_concurrency_filter_values()
        # self.filtered_data_repository.debug_edge_filter_values()
        # self.filtered_data_repository.debug_node_filter_values()
        # Debug block ends

    """
    For applying concurrency filter, can be called directly from front end when user changes value in
    concurrency filter, due to order, it'll call edge filter inherently
    """

    def apply_concurrency_filter(self, concurrency_filter):
        self.config.filter_config.concurrency_filter = concurrency_filter
        self.filtered_data_repository.apply_concurrency_filter(concurrency_filter)
        self.apply_edge_filter(self.config.filter_config.edge_filter)

    """
    For applying edge filter, can be called directly from front end when user changes value in
    edge filter, due to order, it'll call node filter inherently
    """

    def apply_edge_filter(self, edge_filter):
        self.config.filter_config.edge_filter = edge_filter
        self.filtered_data_repository.apply_edge_filter(edge_filter)
        self.apply_node_filter(self.config.filter_config.node_filter)

    """
    For applying node filter, can be called directly from front end when user changes value in
    node filter
    """

    def apply_node_filter(self, node_filter):
        self.config.filter_config.node_filter = node_filter
        self.filtered_data_repository.apply_node_filter(node_filter)
        self.finalize_graph_data()

    def finalize_graph_data(self):
        self.fm_nodes = self.filtered_data_repository.cluster_util.fm_nodes
        self.fm_edges = self.filtered_data_repository.cluster_util.fm_edges
        self.fm_clusters = self.filtered_data_repository.cluster_util.fm_clusters