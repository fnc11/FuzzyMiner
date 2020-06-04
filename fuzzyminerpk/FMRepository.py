import copy
import sys

from fuzzyminerpk.ClusterUtil import ClusterUtil
from fuzzyminerpk.FMUtility import FMLogUtils, is_valid_matrix2D, is_valid_matrix1D, normalize_matrix1D, \
    normalize_matrix2D, cal_endpoint_correlation, cal_originator_correlation, cal_datatype_correlation, \
    cal_datavalue_correlation, cal_proximity_correlation, weight_normalize1D, \
    special_weight_normalize2D, weight_normalize2D


class DataRepository:
    """
    This class object's hold all the extracted data from the log object.

    Instance Attributes:
        log: log object
        config: To hold config object, according to which it extracts data from log object
        fm_log_util: stores basic information about the log object
        nodes: list of primitive nodes (activities) in the log
        num_of_nodes: number of nodes
        node_indices: dictionary to map different nodes to indices in the nodes list
        metric_settings: dictionary to hold different metrics inclusion, inversion and weight data.

        Primary metrics Data:
        unary_node_frequency_values: stores frequency of different nodes(activities)
        unary_node_frequency_normalized: normalized unary_node_frequency_values according to weight specified by user
        binary_edge_frequency_values: stores edge frequency values
        binary_edge_frequency_normalized_values: normalized edge frequency values according to weight
        binary_corr_divisors: stores sum of all attenuation factors for binary correlation metrics.
        binary_corr_proximity_values: stores proximity values of two nodes depending upon the time difference
        binary_corr_proximity_normalized_values: normalized values of proximity values according to weight
        binary_corr_endpoint_values: stores similarity values between two nodes based on activity names
        binary_corr_endpoint_normalized_values: normalized values of endpoint values according to weight
        binary_corr_originator_values: stores similarity values between two nodes based on resource names
        binary_corr_originator_normalized_values: normalized values of originator values according to weight
        binary_corr_datatype_values: stores how much percentage of event keys overlap with the  other event except
        common key values.
        binary_corr_datatype_normalized_values: stores the normalized values of datatype values according to weight
        binary_corr_datavalue_values: stores similarity values between attributes values of two events whose keys match
        in both events except for common keys.
        binary_corr_datavalue_normalized_values: normalized values of the datavalue values according to the weight

        Aggregate Data:
        unary_simple_aggregate_normalized_values: computed using unary_node_frequency_normalized, will be used in
         calculating derivative data (binary distance metric)
        binary_simple_aggregate_normalized_values: computed using binary_edge_frequency_normalized_values, will be used
        in calculating derivative data (unary routing and binary distance metrics)
        binary_multi_aggregate_normalized_values: uses all binary correlation metrics, will be used in calculating
        derivative data (unary routing value)

        Derivative Data:
        unary_derivative_routing_values: holds derivative routing metric values
        unary_derivative_routing_normalized_values: holds normalized unary_derivative_routing_values according to weight
        set by user in metric config.
        binary_derivative_distance_values: holds derivative distance metric values
        binary_derivative_distance_normalized_values: holds normalized binary_derivative_distance_values according to
        weight set by user in metric config.

        Final Data:
        unary_weighted_values: Holds the final node significance values after extracting data according to weights.
        binary_sig_weighted_values: Holds the final edge significance values after extracting data according to weights.
        binary_corr_weighted_values: Holds the final edge correlation values after extracting data according to weights.
    """

    def __init__(self, log, fm_log_util):
        self.log = log
        self.config = None
        self.fm_log_util = fm_log_util
        self.nodes = self.fm_log_util.nodes
        self.num_of_nodes = self.fm_log_util.num_of_nodes
        self.node_indices = self.fm_log_util.node_indices
        self.metric_settings = None

        # initialized all list to None values
        self.unary_node_frequency_values = None
        self.unary_node_frequency_normalized_values = None
        self.binary_corr_divisors = None
        self.binary_edge_frequency_values = None
        self.binary_edge_frequency_normalized_values = None
        self.binary_corr_proximity_values = None
        self.binary_corr_proximity_normalized_values = None
        self.binary_corr_endpoint_values = None
        self.binary_corr_endpoint_normalized_values = None
        self.binary_corr_originator_values = None
        self.binary_corr_originator_normalized_values = None
        self.binary_corr_datatype_values = None
        self.binary_corr_datatype_normalized_values = None
        self.binary_corr_datavalue_values = None
        self.binary_corr_datavalue_normalized_values = None

        self.unary_simple_aggregate_normalized_values = None
        self.binary_simple_aggregate_normalized_values = None
        self.binary_multi_aggregate_normalized_values = None

        self.unary_derivative_routing_values = None
        self.unary_derivative_routing_normalized_values = None
        self.binary_derivative_distance_values = None
        self.binary_derivative_distance_normalized_values = None

        self.unary_weighted_values = None
        self.binary_sig_weighted_values = None
        self.binary_corr_weighted_values = None

    def init_lists(self):
        """
        Initializes all the lists and dictionary which are required to store data to 0 or 0.0
        :return: Nothing
        """

        self.fill_dicts()
        sz = self.num_of_nodes
        self.unary_node_frequency_values = [0 for x in range(sz)]
        self.unary_node_frequency_normalized_values = [0.0 for x in range(sz)]

        self.binary_edge_frequency_values = [[0 for x in range(sz)] for y in range(sz)]
        self.binary_edge_frequency_normalized_values = [[0.0 for x in range(sz)] for y in
                                                        range(sz)]

        self.binary_corr_divisors = [[0.0 for x in range(sz)] for y in
                                     range(sz)]

        self.binary_corr_proximity_values = [[0.0 for x in range(sz)] for y in range(sz)]
        self.binary_corr_proximity_normalized_values = [[0.0 for x in range(sz)] for y in
                                                        range(sz)]

        self.binary_corr_endpoint_values = [[0.0 for x in range(sz)] for y in range(sz)]
        self.binary_corr_endpoint_normalized_values = [[0.0 for x in range(sz)] for y in
                                                       range(sz)]

        self.binary_corr_originator_values = [[0.0 for x in range(sz)] for y in range(sz)]
        self.binary_corr_originator_normalized_values = [[0.0 for x in range(sz)] for y in
                                                         range(sz)]

        self.binary_corr_datatype_values = [[0.0 for x in range(sz)] for y in range(sz)]
        self.binary_corr_datatype_normalized_values = [[0.0 for x in range(sz)] for y in
                                                       range(sz)]

        self.binary_corr_datavalue_values = [[0 for x in range(sz)] for y in range(sz)]
        self.binary_corr_datavalue_normalized_values = [[0.0 for x in range(sz)] for y in
                                                        range(sz)]

        self.unary_simple_aggregate_normalized_values = [0.0 for x in range(sz)]
        self.binary_simple_aggregate_normalized_values = [[0.0 for x in range(sz)] for y in
                                                          range(sz)]
        self.binary_multi_aggregate_normalized_values = [[0.0 for x in range(sz)] for y in
                                                         range(sz)]

        self.unary_derivative_routing_values = [0 for x in range(sz)]
        self.unary_derivative_routing_normalized_values = [0 for x in range(sz)]

        self.binary_derivative_distance_values = [[0 for x in range(sz)] for y in
                                                  range(sz)]
        self.binary_derivative_distance_normalized_values = [[0.0 for x in range(sz)] for y in
                                                             range(sz)]

        self.unary_weighted_values = [0 for x in range(sz)]
        self.binary_sig_weighted_values = [[0 for x in range(sz)] for y in
                                           range(sz)]
        self.binary_corr_weighted_values = [[0 for x in range(sz)] for y in
                                            range(sz)]

    def fill_dicts(self):
        """
        Extracts metric config settings like include, invert and weight, and then stores them
        in a dictionary with their name as key.
        :return: Nothing
        """

        metric_configs = self.config.metric_configs
        self.metric_settings = dict()
        for conf in metric_configs:
            self.metric_settings[conf.name] = (conf.include, conf.invert, conf.weight)

    def extract_primary_metrics(self):
        """
        Extracts all the primary metrics values from the log object and stores them in respective lists
        :return: Nothing
        """

        max_look_back = self.config.maximal_distance
        for trace in self.log:
            look_back = list()
            look_back_indices = list()
            for event in trace:
                follower_event = event
                follower_index = self.node_indices[
                    follower_event['concept:name'] + "@" + follower_event['lifecycle:transition']]
                look_back.insert(0, follower_event)
                look_back_indices.insert(0, follower_index)
                # check to remove extra elements from the list
                # check for out of index error
                if len(look_back) > max_look_back + 1:
                    look_back.pop(max_look_back + 1)
                    look_back_indices.pop(max_look_back + 1)
                # Calculating unary frequency values for the nodes
                self.unary_node_frequency_values[follower_index] += 1
                # Iterating over multi-step relations
                for k in range(1, len(look_back)):
                    ref_event = look_back[k]
                    ref_index = look_back_indices[k]
                    att_factor = self.config.attenuation.get_attenuation_factor(k)

                    # 1 Edge frequency metric
                    self.binary_edge_frequency_values[ref_index][follower_index] += 1.0 * att_factor
                    # 2 Proximity calculation
                    self.binary_corr_proximity_values[ref_index][follower_index] += cal_proximity_correlation(ref_event,
                                                                                                              follower_event) * att_factor
                    # 3 End Point calculation
                    self.binary_corr_endpoint_values[ref_index][follower_index] += cal_endpoint_correlation(ref_event,
                                                                                                            follower_event) * att_factor
                    # 4 Originator calculation
                    self.binary_corr_originator_values[ref_index][follower_index] += cal_originator_correlation(
                        ref_event,
                        follower_event) * att_factor
                    # 5 DataType calculation
                    self.binary_corr_datatype_values[ref_index][follower_index] += cal_datatype_correlation(ref_event,
                                                                                                            follower_event) * att_factor
                    # 6 DataValue calculation
                    self.binary_corr_datavalue_values[ref_index][follower_index] += cal_datavalue_correlation(ref_event,
                                                                                                              follower_event) * att_factor
                    # Since the divisor values are same for all we can just store them once
                    self.binary_corr_divisors[ref_index][follower_index] += att_factor

    def extract_aggregates(self):
        """
        Calls other methods to calculate aggregate values which then will be used in calculating
        derivative metrics
        :return: Nothing
        """

        self.cal_unary_simple_aggregate()
        self.cal_binary_simple_aggregate()
        self.cal_binary_multi_aggregate()

    def extract_derivative_metrics(self):
        """
        Calls other methods to calculate derivative metrics values, routing and distance.
        :return: Nothing
        """

        self.cal_unary_derivative()
        self.cal_binary_derivative()

    def extract_weighted_metrics(self):
        """
        Calls other methods to extract final weighted aggregated values from the normalized metrics according to their
        weight into three separate lists
        :return: Nothing
        """

        self.cal_weighted_unary_values()
        self.cal_weighted_binary_values()
        self.cal_weighted_binary_corr_values()

    def cal_unary_simple_aggregate(self):
        """
        Calculates simple sum of unary normalized values and normalizes them to map max_value to 1. These values will be
        used in calculating derivative binary metrics (distance significance).
        :return: Nothing
        """

        if is_valid_matrix1D(self.unary_node_frequency_normalized_values):
            temp_max = 0
            sz = len(self.unary_node_frequency_normalized_values)
            for i in range(sz):
                self.unary_simple_aggregate_normalized_values[i] = self.unary_node_frequency_normalized_values[i]
                if self.unary_node_frequency_normalized_values[i] > temp_max:
                    temp_max = self.unary_node_frequency_normalized_values[i]
            if temp_max > 0:
                for i in range(sz):
                    # Weighted Normalized to 1
                    self.unary_simple_aggregate_normalized_values[i] *= (1 / temp_max)
        else:
            # since unary_simple_aggregate_normalized_values list is already initialized with 0.0 we don't need to do
            # anything here.
            return

    def cal_binary_simple_aggregate(self):
        """
        Calculates simple sum of binary (excluding binary correlation) normalized values and normalizes them to map
        max_value to 1. These values will be used in calculating derivative unary(routing significance) and derivative
        binary metrics (distance significance)
        :return: Nothing
        """

        if is_valid_matrix2D(self.binary_edge_frequency_normalized_values):
            temp_max = 0
            sz = self.num_of_nodes
            for i in range(0, sz):
                for j in range(0, sz):
                    self.binary_simple_aggregate_normalized_values[i][j] = \
                        self.binary_edge_frequency_normalized_values[i][j]
                    if self.binary_edge_frequency_normalized_values[i][j] > temp_max:
                        temp_max = self.binary_edge_frequency_normalized_values[i][j]
            if temp_max > 0:
                for i in range(0, sz):
                    for j in range(0, sz):
                        # Weighted normalized to 1
                        self.binary_simple_aggregate_normalized_values[i][j] *= (1 / temp_max)
        else:
            # since binary_simple_aggregate_normalized_values list is already initialized with 0.0 we don't need to do
            # anything here.
            return

    def cal_binary_multi_aggregate(self):
        """
        Calculates sum of binary correlation normalized values and normalizes them to map max_value to 1. These values
        will be used in calculating derivative unary metrics (routing significance)
        :return: Nothing
        """

        valid_metrics = list()
        if is_valid_matrix2D(self.binary_corr_proximity_normalized_values):
            valid_metrics.append(self.binary_corr_proximity_normalized_values)
        if is_valid_matrix2D(self.binary_corr_endpoint_normalized_values):
            valid_metrics.append(self.binary_corr_endpoint_normalized_values)
        if is_valid_matrix2D(self.binary_corr_originator_normalized_values):
            valid_metrics.append(self.binary_corr_originator_normalized_values)
        if is_valid_matrix2D(self.binary_corr_datatype_normalized_values):
            valid_metrics.append(self.binary_corr_datatype_normalized_values)
        if is_valid_matrix2D(self.binary_corr_datavalue_normalized_values):
            valid_metrics.append(self.binary_corr_datavalue_normalized_values)

        temp_max = 0
        if len(valid_metrics) > 0:
            sz = self.num_of_nodes
            for i in range(0, sz):
                for j in range(0, sz):
                    aggregated = 0.0
                    for k in range(0, len(valid_metrics)):
                        aggregated += valid_metrics[k][i][j]
                    self.binary_multi_aggregate_normalized_values[i][j] = aggregated
                    if aggregated > temp_max:
                        temp_max = aggregated
            # Normalizing the values now , here we are using 1 as max normalize (weight) to join all the metrics
            if temp_max > 0:
                for i in range(0, sz):
                    for j in range(0, sz):
                        self.binary_multi_aggregate_normalized_values[i][j] *= (1 / temp_max)
        else:
            # since binary_multi_aggregate_normalized_values list is already initialized with 0.0 we don't need to do
            # anything here.
            return

    def cal_unary_derivative(self):
        """
        Calculates derivative unary metric (routing significance) and saves in unary_derivative_routing_values list
        :return: Nothing
        """

        sz = self.num_of_nodes
        for i in range(0, sz):
            in_value = 0.0
            out_value = 0.0
            quotient = 0.0
            for x in range(0, sz):
                if x == i:
                    continue
                in_value += self.binary_simple_aggregate_normalized_values[x][i] * \
                            self.binary_multi_aggregate_normalized_values[x][i]
                out_value += self.binary_simple_aggregate_normalized_values[i][x] * \
                             self.binary_multi_aggregate_normalized_values[i][x]
            if in_value == 0.0 and out_value == 0.0:
                quotient = 0.0
            else:
                quotient = abs((in_value - out_value) / (in_value + out_value))
            self.unary_derivative_routing_values[i] = quotient

    def cal_binary_derivative(self):
        """
        Calculates derivative binary metric (distance significance) and saves in binary_derivative_distance_values list
        :return: Nothing
        """

        sz = self.num_of_nodes
        for i in range(0, sz):
            sig_source = self.unary_simple_aggregate_normalized_values[i]
            for j in range(0, sz):
                sig_target = self.unary_simple_aggregate_normalized_values[j]
                if sig_source + sig_target == 0:
                    continue
                sig_link = self.binary_simple_aggregate_normalized_values[i][j]
                self.binary_derivative_distance_values[i][j] = 1.0 - (
                        (sig_source - sig_link) + (sig_target - sig_link)) / (sig_source + sig_target)

    def normalize_primary_metrics(self):
        """
        Normalizes all the primary metrics according to weights and also inverts the value if specified by user. Saves
        the corresponding values in their respective normalized lists.
        :return: Nothing
        """

        self.unary_node_frequency_normalized_values = weight_normalize1D(self.unary_node_frequency_values,
                                                                         self.metric_settings[
                                                                             "frequency_significance_unary"][1],
                                                                         self.metric_settings[
                                                                             "frequency_significance_unary"][2])
        self.binary_edge_frequency_normalized_values = weight_normalize2D(self.binary_edge_frequency_values,
                                                                          self.metric_settings[
                                                                              "frequency_significance_binary"][1],
                                                                          self.metric_settings[
                                                                              "frequency_significance_binary"][2])
        self.binary_corr_proximity_normalized_values = special_weight_normalize2D(self.binary_corr_proximity_values,
                                                                                  self.binary_corr_divisors,
                                                                                  self.metric_settings[
                                                                                      "proximity_correlation_binary"][
                                                                                      1], self.metric_settings[
                                                                                      "proximity_correlation_binary"][
                                                                                      2])
        self.binary_corr_endpoint_normalized_values = special_weight_normalize2D(self.binary_corr_endpoint_values,
                                                                                 self.binary_corr_divisors,
                                                                                 self.metric_settings[
                                                                                     "endpoint_correlation_binary"][1],
                                                                                 self.metric_settings[
                                                                                     "endpoint_correlation_binary"][2])
        self.binary_corr_originator_normalized_values = special_weight_normalize2D(self.binary_corr_originator_values,
                                                                                   self.binary_corr_divisors,
                                                                                   self.metric_settings[
                                                                                       "originator_correlation_binary"][
                                                                                       1], self.metric_settings[
                                                                                       "originator_correlation_binary"][
                                                                                       2])
        self.binary_corr_datatype_normalized_values = special_weight_normalize2D(self.binary_corr_datatype_values,
                                                                                 self.binary_corr_divisors,
                                                                                 self.metric_settings[
                                                                                     "datatype_correlation_binary"][1],
                                                                                 self.metric_settings[
                                                                                     "datatype_correlation_binary"][2])
        self.binary_corr_datavalue_normalized_values = special_weight_normalize2D(self.binary_corr_datavalue_values,
                                                                                  self.binary_corr_divisors,
                                                                                  self.metric_settings[
                                                                                      "datavalue_correlation_binary"][
                                                                                      1], self.metric_settings[
                                                                                      "datavalue_correlation_binary"][
                                                                                      2])

    def normalize_derivative_metrics(self):
        """
        Normalizes all the derivative metrics according to weights and also inverts the value if specified by user.
        Saves the corresponding values in their respective normalized lists.
        :return: Nothing
        """

        self.unary_derivative_routing_normalized_values = weight_normalize1D(self.unary_derivative_routing_values,
                                                                             self.metric_settings[
                                                                                 "routing_significance_unary"][1],
                                                                             self.metric_settings[
                                                                                 "routing_significance_unary"][2])
        self.binary_derivative_distance_normalized_values = weight_normalize2D(self.binary_derivative_distance_values,
                                                                               self.metric_settings[
                                                                                   "distance_significance_binary"][1],
                                                                               self.metric_settings[
                                                                                   "distance_significance_binary"][2])

    def cal_weighted_unary_values(self):
        """
        Calculates the final unary weighted value (node significance values), on this list filters will be applied
        later. Save the data in unary_weighted_values list.
        :return: Nothing
        """

        inc1 = self.metric_settings["frequency_significance_unary"][0]
        inc2 = self.metric_settings["routing_significance_unary"][0]
        w1 = self.metric_settings["frequency_significance_unary"][2]
        w2 = self.metric_settings["routing_significance_unary"][2]
        sz = self.num_of_nodes
        valid_matrices = list()
        if inc1 and (w1 > 0.0) and is_valid_matrix1D(self.unary_node_frequency_normalized_values):
            valid_matrices.append(self.unary_node_frequency_normalized_values)
        if inc2 and (w2 > 0.0) and is_valid_matrix1D(self.unary_derivative_routing_normalized_values):
            valid_matrices.append(self.unary_derivative_routing_normalized_values)
        for valid_matrix in valid_matrices:
            for i in range(sz):
                self.unary_weighted_values[i] += valid_matrix[i]
        self.unary_weighted_values = normalize_matrix1D(self.unary_weighted_values)

    def cal_weighted_binary_values(self):
        """
        Calculates the final binary weighted value (edge significance values), on this list filters will be applied
        later. Save the data in binary_sig_weighted_values list.
        :return: Nothing
        """

        inc1 = self.metric_settings["frequency_significance_binary"][0]
        inc2 = self.metric_settings["distance_significance_binary"][0]
        w1 = self.metric_settings["frequency_significance_binary"][2]
        w2 = self.metric_settings["distance_significance_binary"][2]
        sz = self.num_of_nodes
        valid_matrices = list()
        if inc1 and (w1 > 0.0) and is_valid_matrix2D(self.binary_edge_frequency_normalized_values):
            valid_matrices.append(self.binary_edge_frequency_normalized_values)
        if inc2 and (w2 > 0.0) and is_valid_matrix2D(self.binary_derivative_distance_normalized_values):
            valid_matrices.append(self.binary_derivative_distance_normalized_values)

        for valid_matrix in valid_matrices:
            for i in range(0, sz):
                for j in range(0, sz):
                    self.binary_sig_weighted_values[i][j] += valid_matrix[i][j]
        self.binary_sig_weighted_values = normalize_matrix2D(self.binary_sig_weighted_values)

    def cal_weighted_binary_corr_values(self):
        """
        Calculates the final binary correlation weighted value (edge correlation values), on this list filters will be
        applied later. Save the data in binary_corr_weighted_values list.
        :return: Nothing
        """
        inc1 = self.metric_settings["proximity_correlation_binary"][0]
        inc2 = self.metric_settings["originator_correlation_binary"][0]
        inc3 = self.metric_settings["endpoint_correlation_binary"][0]
        inc4 = self.metric_settings["datatype_correlation_binary"][0]
        inc5 = self.metric_settings["datavalue_correlation_binary"][0]
        w1 = self.metric_settings["proximity_correlation_binary"][2]
        w2 = self.metric_settings["originator_correlation_binary"][2]
        w3 = self.metric_settings["endpoint_correlation_binary"][2]
        w4 = self.metric_settings["datatype_correlation_binary"][2]
        w5 = self.metric_settings["datavalue_correlation_binary"][2]
        valid_matrices = list()
        if inc1 and (w1 > 0.0) and is_valid_matrix2D(self.binary_corr_proximity_normalized_values):
            valid_matrices.append(self.binary_corr_proximity_normalized_values)
        if inc2 and (w2 > 0.0) and is_valid_matrix2D(self.binary_corr_endpoint_normalized_values):
            valid_matrices.append(self.binary_corr_endpoint_normalized_values)
        if inc3 and (w3 > 0.0) and is_valid_matrix2D(self.binary_corr_originator_normalized_values):
            valid_matrices.append(self.binary_corr_originator_normalized_values)
        if inc4 and (w4 > 0.0) and is_valid_matrix2D(self.binary_corr_datatype_normalized_values):
            valid_matrices.append(self.binary_corr_datatype_normalized_values)
        if inc5 and (w5 > 0.0) and is_valid_matrix2D(self.binary_corr_datavalue_normalized_values):
            valid_matrices.append(self.binary_corr_datavalue_normalized_values)

        sz = self.num_of_nodes

        for valid_matrix in valid_matrices:
            for i in range(0, sz):
                for j in range(0, sz):
                    self.binary_corr_weighted_values[i][j] += valid_matrix[i][j]
        self.binary_corr_weighted_values = normalize_matrix2D(self.binary_corr_weighted_values)

    def debug_print_primary_metric_values(self):
        """
        Debug method to print all the primary metric values.
        :return: Nothing
        """

        print("unary frequency_normalized_values")
        print("this is valid 1D matrix", end=" ")
        print(is_valid_matrix1D(self.unary_node_frequency_normalized_values))
        for val in self.unary_node_frequency_normalized_values:
            print(str(val), end=" ")

        print("\n\n")
        print("Binary edge frequency normalized values")
        print("this is valid 2D matrix", end=" ")
        print(is_valid_matrix2D(self.binary_edge_frequency_normalized_values))
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.binary_edge_frequency_normalized_values[i][j]), end=" ")
            print()

        print("\n\n")
        print("Binary corr proximity_normalized_values")
        print("this is valid 2D matrix", end=" ")
        print(is_valid_matrix2D(self.binary_corr_proximity_normalized_values))
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.binary_corr_proximity_normalized_values[i][j]), end=" ")
            print()
        print()
        print("Binary corr binary_corr_endpoint_normalized_values")
        print("this is valid 2D matrix", end=" ")
        print(is_valid_matrix2D(self.binary_corr_endpoint_normalized_values))
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.binary_corr_endpoint_normalized_values[i][j]), end=" ")
            print()
        print()
        print("Binary corr originator_normalized_values")
        print("this is valid 2D matrix", end=" ")
        print(is_valid_matrix2D(self.binary_corr_originator_normalized_values))
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.binary_corr_originator_normalized_values[i][j]), end=" ")
            print()
        print()
        print("Binary corr datatype_normalized_values")
        print("this is valid 2D matrix", end=" ")
        print(is_valid_matrix2D(self.binary_corr_datatype_normalized_values))
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.binary_corr_datatype_normalized_values[i][j]), end=" ")
            print()
        print()
        print("Binary corr datavalue_normalized_values")
        print("this is valid 2D matrix", end=" ")
        print(is_valid_matrix2D(self.binary_corr_datavalue_normalized_values))
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.binary_corr_datavalue_normalized_values[i][j]), end=" ")
            print()
        print()

    def debug_print_aggregate_values(self):
        """
        Debug method to print all the aggregated values.
        :return: Nothing
        """
        print("Unary simple aggregate values")
        print("this is valid 1D matrix", end=" ")
        print(is_valid_matrix1D(self.unary_node_frequency_values))
        sze = self.num_of_nodes
        for i in range(0, sze):
            print(str(self.unary_simple_aggregate_normalized_values[i]), end=" ")
        print()
        print("Binary simple aggregate values")
        print("this is valid 2D matrix", end=" ")
        print(is_valid_matrix2D(self.binary_edge_frequency_values))
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.binary_simple_aggregate_normalized_values[i][j]), end=" ")
            print()
        print()
        print("Binary simple multi aggregate values")
        print("this is valid 2D matrix", end=" ")
        print(is_valid_matrix2D(self.binary_corr_proximity_normalized_values))
        print(is_valid_matrix2D(self.binary_corr_endpoint_normalized_values))
        print(is_valid_matrix2D(self.binary_corr_originator_normalized_values))
        print(is_valid_matrix2D(self.binary_corr_datatype_normalized_values))
        print(is_valid_matrix2D(self.binary_corr_datavalue_normalized_values))
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.binary_multi_aggregate_normalized_values[i][j]), end=" ")
            print()
        print()

    def debug_print_derivative_metric_values(self):
        """
        Debug method to print all the derivative metric values.
        :return: Nothing
        """
        print("unary_derivative_routing_normalized_values")
        sze = self.num_of_nodes
        for i in range(0, sze):
            print(str(self.unary_derivative_routing_normalized_values[i]), end=" ")
        print()
        print("binary_derivative_distance_normalized_values")
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.binary_derivative_distance_normalized_values[i][j]), end=" ")
            print()
        print()

    def debug_print_weighted_values(self):
        """
        Debug method to print all final weighted values like node significances, edge significances and correlations.
        :return: Nothing
        """
        print("weighted_unary_values")
        sze = self.num_of_nodes
        for i in range(0, sze):
            print(str(self.unary_weighted_values[i]), end=" ")
        print("\n\n")
        print("weighted_binary_values")
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.binary_sig_weighted_values[i][j]), end=" ")
            print()
        print()
        print("weighted_binary_corr_values")
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.binary_corr_weighted_values[i][j]), end=" ")
            print()
        print()


class FilteredDataRepository:
    """
    This class object's hold filtered data after applying different filters.

    Instance Attributes:
        filter_config: Filter configurations
        data_repository: holds extracted data from the log object
        fm_log_util: holds basic information about the log object
        cluster_util: holds ClusterUtil class object to use clusterization functionality and also holds final clusters,
        nodes and edges after clusterization process.
        nodes: list of primitive nodes
        num_of_nodes: number of primitive nodes
        node_indices: Dictionary to hold primitive node indices
        preserve_mask: Used in case of Edge Filers to store which edges survived after filtering
        concurrency_filter_resultant_binary_values: Stores binary edge significance values after applying concurrency
        filter
        concurrency_filter_resultant_binary_corr_values: Stores binary edge correlation values after applying
        concurrency filter
        edge_filter_resultant_binary_values: Stores binary edge significance values after applying edge filter
        edge_filter_resultant_binary_corr_values: Stores binary edge correlation values after applying edge filter
        node_filter_resultant_unary_values: Stores the node significance values, ClusterUtil object need this
        information in order to clusterize.
        node_filter_resultant_binary_values: Stores binary edge significance values after applying node filter
        node_filter_resultant_binary_corr_values: Stores binary edge correlation values after applying node filter

    """

    def __init__(self, fm_log_util):
        """
        Instantiate a filtered repository object.

        :param fm_log_util: fm_log_util object which holds basic information about the log object.
        """
        self.filter_config = None
        self.data_repository = None
        self.fm_log_util = fm_log_util
        self.cluster_util = ClusterUtil()
        self.nodes = self.fm_log_util.nodes
        self.num_of_nodes = self.fm_log_util.num_of_nodes
        self.node_indices = self.fm_log_util.node_indices
        # needed in edge_filtering
        self.preserve_mask = None
        self.concurrency_filter_resultant_binary_values = None
        self.concurrency_filter_resultant_binary_corr_values = None
        self.edge_filter_resultant_binary_values = None
        self.edge_filter_resultant_binary_corr_values = None
        self.node_filter_resultant_unary_values = None
        self.node_filter_resultant_binary_values = None
        self.node_filter_resultant_binary_corr_values = None

    def apply_concurrency_filter(self, concurrency_filter):
        """
        Applies concurrency filter on the data it gets from data_repository and saves the data in the
        concurrency_filter_resultant_binary_values and concurrency_filter_resultant_binary_corr_values lists.
        :param concurrency_filter: new concurrency_filter object
        :return: Nothing
        """

        self.filter_config.concurrency_filter = concurrency_filter
        self.concurrency_filter_resultant_binary_values = copy.deepcopy(self.data_repository.binary_sig_weighted_values)
        self.concurrency_filter_resultant_binary_corr_values = copy.deepcopy(
            self.data_repository.binary_corr_weighted_values)
        if self.filter_config.concurrency_filter.filter_concurrency:
            sz = self.num_of_nodes
            for i in range(0, sz):
                for j in range(0, i):
                    self.process_relation_pair(i, j)

    def process_relation_pair(self, x, y):
        """
        Processes an edge pair for concurrency filter, check according to threshold and ratio values. First checks the
        need of conflict resolution than handles three cases if conflict needs to be resolved:
        1. Both edges are important don't removed any edge.
        2. One of them is important remove the other one which is less important.
        3. Remove both as both are insignificant.
        Saves the values directly in the lists dedicated to store data after applying concurrency filter.
        :param x: source node index
        :param y: destination node index
        :return: Nothing
        """

        sig_fwd = self.data_repository.binary_sig_weighted_values[x][y]
        sig_bwd = self.data_repository.binary_sig_weighted_values[y][x]
        if sig_fwd > 0.0 and sig_bwd > 0.0:
            # need to do conflict resolution
            rel_imp_AB = self.get_relative_imp(x, y)
            rel_imp_BA = self.get_relative_imp(y, x)
            if rel_imp_AB > self.filter_config.concurrency_filter.preserve and rel_imp_BA > self.filter_config.concurrency_filter.preserve:
                return
            else:
                ratio = min(rel_imp_AB, rel_imp_BA) / max(rel_imp_AB, rel_imp_BA)
                if ratio < self.filter_config.concurrency_filter.offset:
                    # preserve one link which has more relative importance
                    if rel_imp_AB > rel_imp_BA:
                        self.concurrency_filter_resultant_binary_values[y][x] = 0.0
                        self.concurrency_filter_resultant_binary_corr_values[y][x] = 0.0
                    else:
                        self.concurrency_filter_resultant_binary_values[x][y] = 0.0
                        self.concurrency_filter_resultant_binary_corr_values[x][y] = 0.0
                else:
                    # both links are not that important, remove both
                    self.concurrency_filter_resultant_binary_values[x][y] = 0.0
                    self.concurrency_filter_resultant_binary_corr_values[x][y] = 0.0
                    self.concurrency_filter_resultant_binary_values[y][x] = 0.0
                    self.concurrency_filter_resultant_binary_corr_values[y][x] = 0.0

    def get_relative_imp(self, x, y):
        """
        Helper method for process_relation_pair it calculates relative importance between two pair of nodes, when given
        their indices.
        :param x: source node index
        :param y: destination node index
        :return: relative importance value
        """

        sig_ref = self.data_repository.binary_sig_weighted_values[x][y]
        sig_source_out = 0.0
        sig_target_in = 0.0
        sz = self.num_of_nodes
        # We reverse the order, need to check if it makes a difference
        for i in range(0, sz):
            if i != x:
                sig_source_out += self.data_repository.binary_sig_weighted_values[x][i]
            if i != y:
                sig_target_in += self.data_repository.binary_sig_weighted_values[i][y]
        return (sig_ref / sig_source_out) + (sig_ref / sig_target_in)

    def apply_edge_filter(self, edge_filter):
        """
        Applies edge filter on the filtered data generated by concurrency filter. Saves the resultant data after applying
        edge filter in edge_filter_resultant_binary_values and edge_filter_resultant_binary_corr_values lists.
        :param edge_filter: new edge_filter object
        :return: Nothing
        """

        self.filter_config.edge_filter = edge_filter
        self.edge_filter_resultant_binary_values = copy.deepcopy(self.concurrency_filter_resultant_binary_values)
        self.edge_filter_resultant_binary_corr_values = copy.deepcopy(
            self.concurrency_filter_resultant_binary_corr_values)
        sz = self.num_of_nodes

        # Initializing an mask for holding true false values
        self.preserve_mask = [[False for x in range(sz)] for y in range(sz)]

        # Return error if something else was sent other than Fuzzy and Best
        if self.filter_config.edge_filter.edge_transform == 1:

            # preserve value can't be zero for filter to generate sensible
            # results, so changing it 0.001 if it is specified zero
            if self.filter_config.edge_filter.preserve == 0.0:
                self.filter_config.edge_filter.preserve = 0.001

            for i in range(0, sz):
                self.process_node_edges_fuzzy_filter(i)
        else:
            for i in range(0, sz):
                self.process_node_edges_best_filter(i)
        for i in range(0, sz):
            for j in range(0, sz):
                if not self.preserve_mask[i][j]:
                    self.edge_filter_resultant_binary_values[i][j] = 0.0
                    self.edge_filter_resultant_binary_corr_values[i][j] = 0.0

    def process_node_edges_fuzzy_filter(self, idx):
        """
        Process edges of specific node according to fuzzy edges filter algorithm. Fills preserve mask value for the
        edges to True if the edges survive after the processing.
        :param idx: index of the node to process
        :return: Nothing
        """

        sz = self.num_of_nodes
        min_in_val = sys.float_info.max
        max_in_val = sys.float_info.min
        min_out_val = sys.float_info.max
        max_out_val = sys.float_info.min
        in_values = [0.0 for i in range(0, sz)]
        out_values = [0.0 for i in range(0, sz)]
        ignore_self_loops = self.filter_config.edge_filter.ignore_self_loops
        sc_ratio = self.filter_config.edge_filter.sc_ratio
        for i in range(0, sz):
            if ignore_self_loops and i == idx:
                continue

            # Check for incoming relations
            significance = self.concurrency_filter_resultant_binary_values[i][idx]
            if significance > 0.0:
                correlation = self.concurrency_filter_resultant_binary_corr_values[i][idx]
                in_values[i] = significance * sc_ratio + correlation * (1.0 - sc_ratio)

                if in_values[i] > max_in_val:
                    max_in_val = in_values[i]
                if in_values[i] < min_in_val:
                    min_in_val = in_values[i]
            else:
                in_values[i] = 0.0

            # check for outgoing relations
            significance = self.concurrency_filter_resultant_binary_values[idx][i]
            if significance > 0.0:
                correlation = self.concurrency_filter_resultant_binary_corr_values[idx][i]
                out_values[i] = significance * sc_ratio + correlation * (1.0 - sc_ratio)

                if out_values[i] > max_out_val:
                    max_out_val = out_values[i]
                if out_values[i] < min_out_val:
                    min_out_val = out_values[i]
            else:
                out_values[i] = 0.0

        if self.filter_config.edge_filter.interpret_abs:
            max_in_val = max(max_in_val, max_out_val)
            max_out_val = max_in_val
            min_in_val = min(min_in_val, min_out_val)
            min_out_val = min_in_val

        in_limit = max_in_val - (max_in_val - min_in_val) * self.filter_config.edge_filter.preserve
        out_limit = max_out_val - (max_out_val - min_out_val) * self.filter_config.edge_filter.preserve

        for i in range(0, sz):
            if ignore_self_loops and i == idx:
                continue
            if in_values[i] >= in_limit:
                self.preserve_mask[i][idx] = True
            if out_values[i] >= out_limit:
                self.preserve_mask[idx][i] = True

    def process_node_edges_best_filter(self, idx):
        """
        Process edges of specific node according to best edges filter algorithm. Fills preserve mask value for the edges
        to True if the edges survive after the processing.
        :param idx: index of the node to process
        :return: Nothing
        """

        # Finding best predecessor and successor of this node
        best_pre = -1
        best_succ = -1
        best_pre_sig = 0.0
        best_succ_sig = 0.0

        sz = self.num_of_nodes

        for i in range(0, sz):
            if i == idx and self.filter_config.edge_filter.ignore_self_loops:
                continue
            pre_sig = self.concurrency_filter_resultant_binary_values[i][idx]
            if pre_sig > best_pre_sig:
                best_pre_sig = pre_sig
                best_pre = i
            succ_sig = self.concurrency_filter_resultant_binary_values[idx][i]
            if succ_sig > best_succ_sig:
                best_succ_sig = succ_sig
                best_succ = i

        if best_pre >= 0:
            self.preserve_mask[best_pre][idx] = True
        if best_succ >= 0:
            self.preserve_mask[idx][best_succ] = True

    def apply_node_filter(self, node_filter):
        """
        Applies node filter on the data which it gets from previous filter (Edge filter). Basically it does the
        clustering operation using clusterize method from cluster_util object for nodes whose significance is less than
        node_filer significance cut_off.
        :param node_filter: new node_filter object to apply
        :return: Nothing
        """

        self.filter_config.node_filter = node_filter
        self.node_filter_resultant_unary_values = copy.deepcopy(self.data_repository.unary_weighted_values)
        self.node_filter_resultant_binary_values = copy.deepcopy(self.edge_filter_resultant_binary_values)
        self.node_filter_resultant_binary_corr_values = copy.deepcopy(self.edge_filter_resultant_binary_corr_values)
        self.cluster_util.clusterize(node_filter, self.fm_log_util, self)

    def debug_concurrency_filter_values(self):
        """
        Debug method to print new edge significance and correlation values after applying the concurrency filter.
        :return: Nothing
        """

        print("concurrency filtered values")
        print("concurrency_filter_resultant_binary_values")
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.concurrency_filter_resultant_binary_values[i][j]), end=" ")
            print()
        print()
        print("concurrency_filter_resultant_binary_corr_values")
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.concurrency_filter_resultant_binary_corr_values[i][j]), end=" ")
            print()
        print()

    def debug_edge_filter_values(self):
        """
        Debug method to print new edge significance and correlation values after applying the edge filter.
        :return: Nothing
        """

        print("edge filtered values")
        print("edge_filter_resultant_binary_values")
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.edge_filter_resultant_binary_values[i][j]), end=" ")
            print()
        print()
        print("edge_filter_resultant_binary_corr_values")
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.edge_filter_resultant_binary_corr_values[i][j]), end=" ")
            print()
        print()

    def debug_node_filter_values(self):
        """
        Debug method to print resultant nodes, clusters and edges after node filtering.
        :return: Nothing
        """

        pass
