import Levenshtein
import numpy as np

from fuzzyminerpk.ClusterUtil import ClusterUtil
from fuzzyminerpk.FMRepository import DataRepository, FilteredDataRepository
from fuzzyminerpk.FMStructure import FMMessage
from fuzzyminerpk.FMUtility import FMLogUtils
from datetime import datetime
import time
from fuzzyminerpk.VizUtil import VizUtil


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
        self.fm_message = FMMessage()

    def apply_config(self, config):
        """ Applies concurrency filter.

        This method is to be called when entire config object is changed, for e.g. during the initiation phase
        or when user changes config in the interface
        """
        # print("Apply Config called with the following config: ")
        # print(config.filter_config)
        # for metric_config in config.metric_configs:
        #     print(metric_config)
        start = time.perf_counter()
        self.config = config
        self.data_repository.config = config
        finish = time.perf_counter()
        self.data_repository.init_lists()
        print(f'Created initial lists in {round(time.perf_counter() - finish, 3)} seconds')
        finish = time.perf_counter()
        self.data_repository.extract_primary_metrics()
        print(f'Extracted primary metrics in {round(time.perf_counter() - finish, 3)} seconds')
        finish = time.perf_counter()
        self.data_repository.normalize_primary_metrics()
        print(f'Normalized primary metrics in {round(time.perf_counter() - finish, 3)} seconds')
        finish = time.perf_counter()
        self.data_repository.extract_aggregates()
        print(f'Extracted aggregated metrics in {round(time.perf_counter() - finish, 3)} seconds')
        finish = time.perf_counter()
        self.data_repository.extract_derivative_metrics()
        print(f'Extracted derivative metrics in {round(time.perf_counter() - finish, 3)} seconds')
        finish = time.perf_counter()
        self.data_repository.normalize_derivative_metrics()
        print(f'Normalized derivative metrics in {round(time.perf_counter() - finish, 3)} seconds')
        finish = time.perf_counter()
        # Final weighted values
        self.data_repository.extract_weighted_metrics()
        print(f'Extracted weighted metrics in {round(time.perf_counter() - finish, 3)} seconds')
        finish = time.perf_counter()
        print(f'Extracted Data in {round(finish-start, 3)} seconds')

        # apply filters on the data
        return self.apply_filters()

    """
    This methods is for first time when we initialize the graph, to apply filters with default values
    """

    def apply_filters(self):
        self.filtered_data_repository.filter_config = self.config.filter_config
        self.filtered_data_repository.data_repository = self.data_repository
        return self.apply_concurrency_filter(self.config.filter_config.concurrency_filter)

        # Just for debug purpose
        # Debug block starts
        # self.filtered_data_repository.debug_concurrency_filter_values()
        # self.filtered_data_repository.debug_edge_filter_values()
        # self.filtered_data_repository.debug_node_filter_values()
        # Debug block ends

    def apply_concurrency_filter(self, concurrency_filter):
        """ Returns a FMMessage.

        For applying concurrency filter, can be called directly from front end when user changes value in
        concurrency filter, due to order, it'll call edge filter inherently
        """
        # print("Apply Concurrency filter is called with following values: ")
        # print(concurrency_filter)
        self.config.filter_config.concurrency_filter = concurrency_filter
        self.filtered_data_repository.apply_concurrency_filter(concurrency_filter)
        return self.apply_edge_filter(self.config.filter_config.edge_filter)

    def apply_edge_filter(self, edge_filter):
        """ Returns a FMMessage.

        For applying edge filter, can be called directly from front end when user changes value in
        edge filter, due to order, it'll call node filter inherently
        """
        # print("Apply Edge filter is called with following values: ")
        # print(edge_filter)
        self.config.filter_config.edge_filter = edge_filter
        self.filtered_data_repository.apply_edge_filter(edge_filter)
        return self.apply_node_filter(self.config.filter_config.node_filter)

    def apply_node_filter(self, node_filter):
        """ Returns a FMMessage.

        For applying node filter, can be called directly from front end when user changes value in
        node filter
        """
        # print("Apply Node filter is called with following values: " + "\n")
        # print(node_filter)
        self.config.filter_config.node_filter = node_filter
        self.filtered_data_repository.apply_node_filter(node_filter)
        self.finalize_graph_data()
        self.check_for_null_graph()
        if self.fm_message.message_type == 0:
            # Generate graph and save the path
            self.viz_util = VizUtil()
            graph_path = self.viz_util.visualize(self.fm_nodes, self.fm_edges, self.fm_clusters)
            self.fm_message.graph_path = graph_path

        return self.fm_message

    def finalize_graph_data(self):
        self.fm_nodes = self.filtered_data_repository.cluster_util.fm_nodes
        self.fm_edges = self.filtered_data_repository.cluster_util.fm_edges
        self.fm_clusters = self.filtered_data_repository.cluster_util.fm_clusters

        # Just for debug purpose
        # Debug block starts
        # print("Nodes\n")
        # for node in self.fm_nodes:
        #     print(node)
        #     print()
        #
        # print("\nClusters\n")
        # for cluster in self.fm_clusters:
        #     print(cluster)
        #     print()
        #
        # print("\nEdges\n")
        # for edge in self.fm_edges:
        #     print(edge)
        #     print()
        # self.data_repository.debug_print_primary_metric_values()
        # self.data_repository.debug_print_aggregate_values()
        # self.data_repository.debug_print_derivative_metric_values()
        # self.data_repository.debug_print_weighted_values()
        # Debug block ends

    def check_for_null_graph(self):
        if len(self.fm_nodes) == 0:
            self.fm_message.message_type == 2
            self.fm_message.message_desc == "The current config and filter settings resulted either a null graph or one cluster. Please try changing config or filters or both."

    def apply_metrics_config(self, metrics_configs, attenuation, chunk_size):
        # print("Apply Metrics config is called with following values: ")
        # for metrics_config in metrics_configs:
        #     print(metrics_config)
        # print(attenuation)
        # print("\nMaximum Distance: " + str(chunk_size))
        self.config.metrics_configs = metrics_configs
        self.config.attenuation = attenuation
        self.config.chunk_size = chunk_size
        return self.apply_config(self.config)
