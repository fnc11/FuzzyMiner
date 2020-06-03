from fuzzyminerpk.ClusterUtil import ClusterUtil
from fuzzyminerpk.FMRepository import DataRepository, FilteredDataRepository
from fuzzyminerpk.FMStructure import FMMessage
from fuzzyminerpk.FMUtility import FMLogUtils
from fuzzyminerpk.VizUtil import VizUtil

import time


class Graph:
    """
    Class to generate FuzzyGraph from Log object (converted using xes importer from log file).

    Instance Attributes:
    config: stores the configuration object
    fm_log_util: fm_log_util object contains basic information about activities in the log object
    cluster_util: used to form clusters
    data_repository: contains all the metrics data extracted from log object
    filtered_data_repository: contains all the data after applying different filters on the metrics data
    fm_nodes: Holds list of final nodes generated after applying the configuration of metrics and filters
    fm_edges: Holds list of final edges generated after applying the configuration of metrics and filters
    fm_clusters: Holds list of final clusters generated after applying the configuration of metrics and filters
    fm_message: Holds all the different error types which can happen while performing all the different actions,
     which contains message_type, message_desc and graph_path(if graph generated successfully)

    """

    def __init__(self, log):
        """
        Instantiates a graph object
        :param log: log object which is parsed using xes importer on log file.
        """
        self.config = None
        self.fm_log_util = FMLogUtils(log)
        self.cluster_util = ClusterUtil()
        self.data_repository = DataRepository(log, self.fm_log_util)
        self.filtered_data_repository = FilteredDataRepository(self.fm_log_util)
        self.fm_nodes = None
        self.fm_clusters = None
        self.fm_edges = None
        self.fm_message = FMMessage()

    def apply_config(self, config):
        """
        This method is to be called when entire config object is changed, for e.g. during the initiation phase
        or when user changes config in the interface.

        :param config: new configuration which is to be applied on the graph.
        :return: fm_message
        """
        # print("Apply Config called with the following config: ")
        # print(config.filter_config)
        # for metric_config in config.metric_configs:
        #     print(metric_config)
        start = time.perf_counter()
        self.config = config
        self.data_repository.config = config
        self.data_repository.init_lists()
        self.data_repository.extract_primary_metrics()
        self.data_repository.normalize_primary_metrics()
        self.data_repository.extract_aggregates()
        self.data_repository.extract_derivative_metrics()
        self.data_repository.normalize_derivative_metrics()
        # Final weighted values
        self.data_repository.extract_weighted_metrics()
        finish = time.perf_counter()
        print(f'Extracted Data in {round(finish - start, 3)} seconds')

        # apply filters on the data
        return self.apply_filters()

    def apply_filters(self):
        """
        This methods is for first time when we initialize the graph, to apply filters with values supplied
        with initial configuration or which is currently present in the object

        :return: fm_message
        """
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
        """
        This method applies concurrency filter, due to order, it'll call edge filter next.

        :param concurrency_filter: new concurrency filter object or the value stored in config
        :return: fm_message
        """
        # print("Apply Concurrency filter is called with following values: ")
        # print(concurrency_filter)
        self.config.filter_config.concurrency_filter = concurrency_filter
        self.filtered_data_repository.apply_concurrency_filter(concurrency_filter)
        return self.apply_edge_filter(self.config.filter_config.edge_filter)

    def apply_edge_filter(self, edge_filter):
        """
        This method applies edge filter, due to order, it'll call node filter next.

        :param edge_filter: new edge filter object or the value stored in config
        :return: fm_message
        """
        # print("Apply Edge filter is called with following values: ")
        # print(edge_filter)
        self.config.filter_config.edge_filter = edge_filter
        self.filtered_data_repository.apply_edge_filter(edge_filter)
        return self.apply_node_filter(self.config.filter_config.node_filter)

    def apply_node_filter(self, node_filter):
        """
        This method applies node filter, and since applying node filter means clusterization also.
        After this method all the graph related data is finalized like fm_nodes, fm_clusters and fm_edges.
        :param node_filter: new node filter object or the value stored in config
        :return: fm_message
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
        """
        Finalises graph data which can be used to draw graph, like nodes, edges, clusters etc.
        :return: None
        """
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
        """
        Checks if the graph generated has one node or one cluster or both of them is zero then it sets the error
        message to type 2, which means that the user's selected configuration is not good to visualize the process
        he/should change it.
        :return: None
        """
        if len(self.fm_nodes) + len(self.fm_clusters) <= 1:
            self.fm_message.message_type == 2
            self.fm_message.message_desc == "The current config and filter settings resulted either a null graph or one cluster. Please try changing config or filters or both."

    def apply_metrics_config(self, metrics_configs, attenuation, maximal_distance):
        """
        Applies new metric configuration, attenuation and maximal distance size on the graph object
        :param metrics_configs: new metric configuration object
        :param attenuation: new attenuation object
        :param maximal_distance: new distance upto which fuzzy relations to be considered
        :return: fm_message
        """
        # print("Apply Metrics config is called with following values: ")
        # for metrics_config in metrics_configs:
        #     print(metrics_config)
        # print(attenuation)
        # print("\nMaximum Distance: " + str(chunk_size))
        self.config.metrics_configs = metrics_configs
        self.config.attenuation = attenuation
        self.config.maximal_distance = maximal_distance
        return self.apply_config(self.config)
