from fuzzyminerpk.Utility import FMLogUtils, is_valid_matrix2D, is_valid_matrix1D, normalize_matrix1D, normalize_matrix2D, cal_endpoint_correlation, cal_originator_correlation, cal_datatype_correlation, cal_datavalue_correlation, cal_proximity_correlation


class DataRepository:
    def __init__(self, log, config):
        self.log = log
        self.config = config
        self.fm_log_util = FMLogUtils(log)
        self.nodes = self.fm_log_util.nodes
        self.num_of_nodes = self.fm_log_util.num_of_nodes
        self.node_indices = self.fm_log_util.node_indices

        # declare lists to store data
        self.unary_node_frequency_values = list()
        self.unary_node_frequency_normalized_values = list()

        self.binary_edge_frequency_values = list()
        self.binary_edge_frequency_divisors = list()
        self.binary_edge_frequency_normalized_values = list()

        self.binary_corr_proximity_values = list()
        self.binary_corr_proximity_divisors = list()
        self.binary_corr_proximity_normalized_values = list()

        self.binary_corr_endpoint_values = list()
        self.binary_corr_endpoint_divisors = list()
        self.binary_corr_endpoint_normalized_values = list()

        self.binary_corr_originator_values = list()
        self.binary_corr_originator_divisors = list()
        self.binary_corr_originator_normalized_values = list()

        self.binary_corr_datatype_values = list()
        self.binary_corr_datatype_divisors = list()
        self.binary_corr_datatype_normalized_values = list()

        self.binary_corr_datavalue_values = list()
        self.binary_corr_datavalue_divisors = list()
        self.binary_corr_datavalue_normalized_values = list()

        ###########Aggregate(simple sum)########
        # unary aggregate computation - used frequency significance, will be used in cal distance
        self.unary_simple_aggregate_normalized_values = list()
        # binary aggregate computation - used frequency significance, will be used in cal routing_significance and distance
        self.binary_simple_aggregate_normalized_values = list()
        # binary aggregate multiple computation - used all binary corr metrics, will be used in cal routing_significance
        self.binary_simple_multi_aggregate_normalized_values = list()

        ###########Derivative metrices######
        self.unary_derivative_routing_values = list()
        self.unary_derivative_routing_normalized_values = list()

        self.binary_derivative_distance_values = list()
        self.binary_derivative_distance_divisors = list()

        ###########Weighted metrics######
        self.unary_weighted_values = list()
        self.binary_weighted_values = list()
        self.binary_corr_weighted_values = list()

        # initialize empty lists
        self.init_lists()

        # dictionary to save weights, invert, include
        self.metric_settings = dict()
        self.fill_dicts()

    """
    This initializes all the lists which are required to store data to 0 or 0.0, in special cases to 1.0
    """

    def init_lists(self):
        self.unary_node_frequency_values = [0 for x in range(self.num_of_nodes)]
        self.unary_node_frequency_normalized_values = [0 for x in range(self.num_of_nodes)]

        self.binary_edge_frequency_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_edge_frequency_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                               range(self.num_of_nodes)]
        self.binary_edge_frequency_normalized_values = [[0.0 for x in range(self.num_of_nodes)] for y in
                                                        range(self.num_of_nodes)]

        self.binary_corr_proximity_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_corr_proximity_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                               range(self.num_of_nodes)]
        self.binary_corr_proximity_normalized_values = [[0.0 for x in range(self.num_of_nodes)] for y in
                                                        range(self.num_of_nodes)]

        self.binary_corr_endpoint_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_corr_endpoint_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                              range(self.num_of_nodes)]
        self.binary_corr_endpoint_normalized_values = [[0.0 for x in range(self.num_of_nodes)] for y in
                                                       range(self.num_of_nodes)]

        self.binary_corr_originator_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_corr_originator_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                range(self.num_of_nodes)]
        self.binary_corr_originator_normalized_values = [[0.0 for x in range(self.num_of_nodes)] for y in
                                                         range(self.num_of_nodes)]

        self.binary_corr_datatype_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_corr_datatype_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                              range(self.num_of_nodes)]
        self.binary_corr_datatype_normalized_values = [[0.0 for x in range(self.num_of_nodes)] for y in
                                                       range(self.num_of_nodes)]

        self.binary_corr_datavalue_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_corr_datavalue_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                               range(self.num_of_nodes)]
        self.binary_corr_datavalue_normalized_values = [[0.0 for x in range(self.num_of_nodes)] for y in
                                                        range(self.num_of_nodes)]

        ###########Aggregate(simple sum)########
        # unary aggregate computation - used frequency significance, will be used in cal distance
        self.unary_simple_aggregate_normalized_values = [0.0 for x in range(self.num_of_nodes)]

        # binary aggregate computation - used frequency significance, will be used in cal routing_significance and distance
        self.binary_simple_aggregate_normalized_values = [[0.0 for x in range(self.num_of_nodes)] for y in
                                                          range(self.num_of_nodes)]

        # binary aggregate multiple computation - used all binary corr metrics, will be used in cal routing_significance
        self.binary_simple_multi_aggregate_normalized_values = [[0.0 for x in range(self.num_of_nodes)] for y in
                                                                range(self.num_of_nodes)]

        ###########Derivative metrices######
        self.unary_derivative_routing_values = [0 for x in range(self.num_of_nodes)]
        self.unary_derivative_routing_normalized_values = [0 for x in range(self.num_of_nodes)]

        self.binary_derivative_distance_values = [[0 for x in range(self.num_of_nodes)] for y in
                                                  range(self.num_of_nodes)]
        self.binary_derivative_distance_normalized_values = [[0.0 for x in range(self.num_of_nodes)] for y in
                                                             range(self.num_of_nodes)]

        ########Weighted lists###########
        self.unary_weighted_values = [0 for x in range(self.num_of_nodes)]
        self.binary_weighted_values = [[0 for x in range(self.num_of_nodes)] for y in
                                       range(self.num_of_nodes)]
        self.binary_corr_weighted_values = [[0 for x in range(self.num_of_nodes)] for y in
                                            range(self.num_of_nodes)]

    """
    This method extract metric config settings like include, invert and weight, and then stores them
    in a dictionary with their name as key.
    """

    def fill_dicts(self):
        metric_configs = self.config.metric_configs
        for conf in metric_configs:
            self.metric_settings[conf.name] = (conf.include, conf.invert, conf.weight)

    """
    This extracts all the primary metrics values from the log object
    """

    def extract_primary_metrics(self):
        max_look_back = self.config.chunk_size
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
                    self.binary_edge_frequency_divisors[ref_index][follower_index] += att_factor

                    # 2 Proximity calculation
                    self.binary_corr_proximity_values[ref_index][follower_index] += cal_proximity_correlation(ref_event,
                                                                                                  follower_event) * att_factor
                    self.binary_corr_proximity_divisors[ref_index][follower_index] += att_factor

                    # 3 End Point calculation
                    self.binary_corr_endpoint_values[ref_index][follower_index] += cal_endpoint_correlation(ref_event,
                                                                                                follower_event) * att_factor
                    self.binary_corr_endpoint_divisors[ref_index][follower_index] += att_factor

                    # 4 Originator calculation
                    self.binary_corr_originator_values[ref_index][follower_index] += cal_originator_correlation(ref_event,
                                                                                                    follower_event) * att_factor
                    self.binary_corr_originator_divisors[ref_index][follower_index] += att_factor

                    # 5 DataType calculation
                    self.binary_corr_datatype_values[ref_index][follower_index] += cal_datatype_correlation(ref_event,
                                                                                                follower_event) * att_factor
                    self.binary_corr_datatype_divisors[ref_index][follower_index] += att_factor

                    # 6 DataValue calculation
                    self.binary_corr_datavalue_values[ref_index][follower_index] += cal_datavalue_correlation(ref_event,
                                                                                                  follower_event) * att_factor
                    self.binary_corr_datavalue_divisors[ref_index][follower_index] += att_factor

    """
    This methods calls other methods to calculate aggregate values which is used in calculating
    derivative metrics
    """

    def extract_simple_aggregates(self):
        self.cal_unary_simple_aggregate()
        self.cal_binary_simple_aggregate()
        self.cal_binary_simple_multi_aggregate()

    """
    This methods calls other methods to calculate derivative metrics values, routing and distance.
    """

    def extract_derivative_metrics(self):
        self.cal_unary_derivative()
        self.cal_binary_derivative()

    """
    To extract weighted values from the normalized metrics according to their weight into three separate lists
    """

    def extract_weighted_metrics(self):
        self.cal_weighted_unary_values()
        self.cal_weighted_binary_values()
        self.cal_wrighted_binary_corr_values()

    """
    This function calculates simple sum of unary metrics values/normalized which is used in 
    calculating derivative binary metrics (distance significance)
    """

    def cal_unary_simple_aggregate(self):
        ## Caution Use normalized value of all the metrics
        if is_valid_matrix1D(self.unary_node_frequency_values):
            ##Caution for this zero value
            temp_max = 0
            for i in range(0, len(self.unary_node_frequency_values)):
                self.unary_simple_aggregate_normalized_values[i] = self.unary_node_frequency_values[i]
                if self.unary_node_frequency_values[i] > temp_max:
                    temp_max = self.unary_node_frequency_values[i]
            if temp_max > 0:
                for i in range(0, len(self.unary_node_frequency_values)):
                    # Note: Could also fill normalized list self.binary_edge_frequency_normalized_values
                    self.unary_simple_aggregate_normalized_values[i] *= (1 / temp_max)
        else:
            ##Caution: Check if we need to return or do somthing else
            return

    """
    This function calculates simple sum of binary metrics values/normalized which is used in 
    calculating derivative unary(routing significance) and derivative binary metrics (distance significance)
    """

    def cal_binary_simple_aggregate(self):
        ## Caution Use normalized value of all the metrics
        if is_valid_matrix2D(self.binary_edge_frequency_values):
            ##Caution for this zero value
            temp_max = 0
            sz = self.num_of_nodes
            for i in range(0, sz):
                for j in range(0, sz):
                    self.binary_simple_aggregate_normalized_values[i][j] = self.binary_edge_frequency_values[i][j]
                    if self.binary_edge_frequency_values[i][j] > temp_max:
                        temp_max = self.binary_edge_frequency_values[i][j]
            if temp_max > 0:
                for i in range(0, sz):
                    for j in range(0, sz):
                        # Note: Could also fill normalized list self.binary_edge_frequency_normalized_values
                        self.binary_simple_aggregate_normalized_values[i][j] *= (1 / temp_max)
        else:
            ##Caution: Check if we need to return or do somthing else
            return

    """
    This function calculates sum of binary metrics values/normalized which is used in 
    calculating derivative unary metrics (routing significance)
    """

    def cal_binary_simple_multi_aggregate(self):
        # Will be used for correlating related metric aggregation
        ##Reminder Check if these metrics were normalized
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
        ##Caution for this zero value
        temp_max = 0
        if len(valid_metrics) > 0:
            # print("valid metrics are :"+str(len(valid_metrics)))
            sz = self.num_of_nodes
            for i in range(0, sz):
                for j in range(0, sz):
                    aggregated = 0.0
                    for k in range(0, len(valid_metrics)):
                        # Check if this below code is accessing values correctly
                        # print("Accessed value: "+str(valid_metrics[k][i][j]))
                        aggregated += valid_metrics[k][i][j]
                    # print("Aggregated sum : "+str(aggregated))
                    self.binary_simple_multi_aggregate_normalized_values[i][j] = aggregated
                    if aggregated > temp_max:
                        temp_max = aggregated
            if temp_max > 0:
                for i in range(0, sz):
                    for j in range(0, sz):
                        self.binary_simple_multi_aggregate_normalized_values[i][j] *= (1 / temp_max)
        else:
            ##Caution: Check if we need to return or do somthing else
            return

    """
    This calculates routing significance metric.
    """

    def cal_unary_derivative(self):
        sz = self.num_of_nodes
        for i in range(0, sz):
            in_value = 0.0
            out_value = 0.0
            quotient = 0.0
            for x in range(0, sz):
                if x == i:
                    continue
                in_value += self.binary_simple_aggregate_normalized_values[x][i] * \
                            self.binary_simple_multi_aggregate_normalized_values[x][i]
                out_value += self.binary_simple_aggregate_normalized_values[i][x] * \
                             self.binary_simple_multi_aggregate_normalized_values[i][x]
            if in_value == 0.0 and out_value == 0.0:
                quotient = 0.0
            else:
                quotient = abs((in_value - out_value) / (in_value + out_value))
            self.unary_derivative_routing_values[i] = quotient

    """
    This calculates distance significance metric.
    """

    def cal_binary_derivative(self):
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

    """
    Normalizes all the primary metrics.
    """

    def normalize_primary_metrics(self):
        self.unary_node_frequency_normalized_values = normalize_matrix1D(self.unary_node_frequency_values)
        self.binary_edge_frequency_normalized_values = normalize_matrix2D(self.binary_edge_frequency_values)
        self.binary_corr_proximity_normalized_values = normalize_matrix2D(self.binary_corr_proximity_values)
        self.binary_corr_endpoint_normalized_values = normalize_matrix2D(self.binary_corr_endpoint_values)
        self.binary_corr_originator_normalized_values = normalize_matrix2D(self.binary_corr_originator_values)
        self.binary_corr_datatype_normalized_values = normalize_matrix2D(self.binary_corr_datatype_values)
        self.binary_corr_datavalue_normalized_values = normalize_matrix2D(self.binary_corr_datavalue_values)

    """
    Normalized all the derivative metrics, routing and distance.
    """

    def normalize_derivative_metrics(self):
        self.unary_derivative_routing_normalized_values = normalize_matrix1D(self.unary_derivative_routing_values)
        self.binary_derivative_distance_normalized_values = normalize_matrix2D(self.binary_derivative_distance_values)

    """
    For calculating unary weighted values
    Invert functionality still missing
    """

    def cal_weighted_unary_values(self):
        inc1 = self.metric_settings["frequency_significance_unary"][0]
        inc2 = self.metric_settings["routing_significance_unary"][0]

        w1 = self.metric_settings["frequency_significance_unary"][2] if inc1 else 0.0
        w2 = self.metric_settings["routing_significance_unary"][2] if inc2 else 0.0

        inv1 = self.metric_settings["frequency_significance_unary"][1]
        inv2 = self.metric_settings["routing_significance_unary"][1]

        sz = self.num_of_nodes
        # if single metrics is selected then weight factor doesn't take effect
        if inv1 and not inv2:
            w1 = 1 - w1
        elif not inv1 and inv2:
            w2 = 1 - w2
        elif inv1 and inv2:
            w1 = 1 - w1
            w2 = 1 - w2

        if w1 + w2 != 0:
            for i in range(0, sz):
                self.unary_weighted_values = [(val1 * w1 + val2 * w2) / (w1 + w2) for val1, val2
                                              in zip(self.unary_node_frequency_normalized_values,
                                                     self.unary_derivative_routing_normalized_values)]

    """
    For calculating binary weighted values
    Invert functionality still missing
    """

    def cal_weighted_binary_values(self):
        inc1 = self.metric_settings["frequency_significance_binary"][0]
        inc2 = self.metric_settings["distance_significance_binary"][0]

        w1 = self.metric_settings["frequency_significance_binary"][2] if inc1 else 0.0
        w2 = self.metric_settings["distance_significance_binary"][2] if inc2 else 0.0

        inv1 = self.metric_settings["frequency_significance_binary"][1]
        inv2 = self.metric_settings["distance_significance_binary"][1]

        sz = self.num_of_nodes

        ## if single metrics is selected then weight factor doesn't take effect
        if inv1 and not inv2:
            w1 = 1 - w1
        elif not inv1 and inv2:
            w2 = 1 - w2
        elif inv1 and inv2:
            w1 = 1 - w1
            w2 = 1 - w2
        if w1 + w2 != 0.0:
            binary_weight_values = list()
            for i in range(0, sz):
                temp_list = list()
                for j in range(0, sz):
                    temp_list.append((self.binary_edge_frequency_normalized_values[i][j] * w1 +
                                      self.binary_derivative_distance_normalized_values[i][j] * w2) / (w1 + w2))
                binary_weight_values.append(temp_list)
            self.binary_weighted_values = binary_weight_values

    """
    For calculating binary corrleation weighted values
    Invert functionality still missing
    """

    def cal_wrighted_binary_corr_values(self):
        inc1 = self.metric_settings["proximity_correlation_binary"][0]
        inc2 = self.metric_settings["originator_correlation_binary"][0]
        inc3 = self.metric_settings["endpoint_correlation_binary"][0]
        inc4 = self.metric_settings["datatype_correlation_binary"][0]
        inc5 = self.metric_settings["datavalue_correlation_binary"][0]

        w1 = self.metric_settings["proximity_correlation_binary"][2] if inc1 else 0.0
        w2 = self.metric_settings["originator_correlation_binary"][2] if inc2 else 0.0
        w3 = self.metric_settings["endpoint_correlation_binary"][2] if inc3 else 0.0
        w4 = self.metric_settings["datatype_correlation_binary"][2] if inc4 else 0.0
        w5 = self.metric_settings["datavalue_correlation_binary"][2] if inc5 else 0.0

        inv1 = self.metric_settings["proximity_correlation_binary"][1]
        inv2 = self.metric_settings["originator_correlation_binary"][1]
        inv3 = self.metric_settings["endpoint_correlation_binary"][1]
        inv4 = self.metric_settings["datatype_correlation_binary"][1]
        inv5 = self.metric_settings["datavalue_correlation_binary"][1]

        sz = self.num_of_nodes

        ## if single metrics is selected then weight factor doesn't take effect
        if inv1:
            w1 = 1 - w1

        if inv2:
            w2 = 1 - w2

        if inv3:
            w3 = 1 - w3

        if inv4:
            w4 = 1 - w4

        if inv5:
            w5 = 1 - w5

        if w1 + w2 + w3 + w4 + w5 != 0.0:
            binary_corr_weight_values = list()
            for i in range(0, sz):
                temp_list = list()
                for j in range(0, sz):
                    temp_list.append((self.binary_corr_proximity_normalized_values[i][j] * w1 +
                                      self.binary_corr_originator_normalized_values[i][j] * w2 +
                                      self.binary_corr_endpoint_normalized_values[i][j] * w3 +
                                      self.binary_corr_datatype_normalized_values[i][j] * w4 +
                                      self.binary_corr_datavalue_normalized_values[i][j] * w5) / (
                                             w1 + w2 + w3 + w4 + w5))
                binary_corr_weight_values.append(temp_list)
            self.binary_corr_weighted_values = binary_corr_weight_values

    def debug_print_primary_metric_values(self):
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
                print(str(self.binary_simple_multi_aggregate_normalized_values[i][j]), end=" ")
            print()
        print()

    def debug_print_derivative_metric_values(self):
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
        print("weighted_unary_values")
        sze = self.num_of_nodes
        for i in range(0, sze):
            print(str(self.unary_weighted_values[i]), end=" ")
        print("\n\n")
        print("weighted_binary_values")
        sze = self.num_of_nodes
        for i in range(0, sze):
            for j in range(0, sze):
                print(str(self.binary_weighted_values[i][j]), end=" ")
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
    def __init__(self, log, data_repository, filter_config):
        self.filter_config = filter_config
        self.data_repository = data_repository
        self.fm_log_util = FMLogUtils(log)
        self.log = log
        self.nodes = self.fm_log_util.nodes
        self.num_of_nodes = self.fm_log_util.num_of_nodes
        self.node_indices = self.fm_log_util.node_indices
        self.concurrency_filter_resultant_binary_values = list()
        self.concurrency_filter_resultant_binary_corr_values = list()
        self.preserve_mask = list()  # needed in edge_filtering
        self.edge_filter_resultant_binary_values = list()
        self.edge_filter_resultant_binary_corr_values = list()
        self.node_filter_resultant_binary_values = list()
        self.node_filter_resultant_binary_corr_values = list()

    """
    Applies concurrency_filter and then calls implicitly edge_filter to apply
    """

    def apply_concurrency_filter(self, concurrency_filter):
        self.filter_config.concurrency_filter = concurrency_filter
        self.concurrency_filter_resultant_binary_values = self.data_repository.binary_weighted_values
        self.concurrency_filter_resultant_binary_corr_values = self.data_repository.binary_corr_weighted_values
        if self.filter_config.concurrency_filter.filter_concurrency:
            sz = self.num_of_nodes
            for i in range(0, sz):
                for j in range(0, i):
                    self.process_relation_pair(i, j)
            # Applying edge_filter with older values(since only values of concurrency_filter was changed)
            # call method based on type of filter selected fuzzy or best edge(by default it's fuzzy edge filter)
            self.apply_edge_filter(self.filter_config.edge_filter)
        else:
            self.apply_edge_filter(self.filter_config.edge_filter)

    """
    To process an edge pair for concurrency filter, check according to threshold and ratio values.
    """

    def process_relation_pair(self, x, y):
        sig_fwd = self.data_repository.binary_weighted_values[x][y]
        sig_bwd = self.data_repository.binary_weighted_values[y][x]
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

    """
    Helper method for process_relation_pair, it calculates relative importance 
    between two pair of nodes, when given their indices.
    """

    def get_relative_imp(self, x, y):
        sig_ref = self.data_repository.binary_weighted_values[x][y]
        sig_source_out = 0.0
        sig_target_in = 0.0
        sz = self.num_of_nodes
        # We reverse the order, need to check if it makes a difference
        for i in range(0, sz):
            if i != x:
                sig_source_out += self.data_repository.binary_weighted_values[x][i]
            if i != y:
                sig_target_in += self.data_repository.binary_weighted_values[i][x]
        return (sig_ref / sig_source_out) + (sig_ref / sig_target_in)

    """
    Applies edge_filter according to selected type Fuzzy or Best and then implicitly calls node_filter to apply
    """

    def apply_edge_filter(self, edge_filter):
        self.filter_config.edge_filter = edge_filter
        self.edge_filter_resultant_binary_values = self.concurrency_filter_resultant_binary_values
        self.edge_filter_resultant_binary_corr_values = self.concurrency_filter_resultant_binary_corr_values
        sz = self.num_of_nodes
        # Initializing an mask for holding true false values
        self.preserve_mask = [[False for x in range(sz)] for y in range(sz)]
        ## Return error if something else was sent other than Fuzzy and Best
        if edge_filter.edge_transform == "Fuzzy":
            for i in range(0, sz):
                self.process_node_edges_fuzzy_filter(i)
        else:
            for i in range(0, sz):
                self.process_node_edges_best_filter(i)
        for i in range(0, sz):
            for j in range(0, sz):
                if i == j:
                    continue
                if not self.preserve_mask[i][j]:
                    self.edge_filter_resultant_binary_values[i][j] = 0.0
                    self.edge_filter_resultant_binary_corr_values[i][j] = 0.0

        # Applying node_filter with older values(since only values of edge_filter or concurrency_filter was changed)
        self.apply_node_filter(self.filter_config.node_filter)

    """
    Processes edges of nodes one by one, checks according to sc_ratio, cut_off and other attributes.
    """

    def process_node_edges_fuzzy_filter(self, idx):
        sz = self.num_of_nodes
        min_in_val = float('inf')
        max_in_val = float('-inf')
        min_out_val = float('inf')
        max_out_val = float('-inf')
        in_values = [0.0 for i in range(0, sz)]
        out_values = [0.0 for i in range(0, sz)]
        ignore_self_loops = self.filter_config.edge_filter.ignore_self_loops
        sc_ratio = self.filter_config.edge_filter.sc_ratio
        for i in range(0, sz):
            if ignore_self_loops and i == idx:
                # do nothing
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
            min_in_val = max(min_in_val, min_out_val)
            min_out_val = min_in_val
        in_limit = max_in_val - (max_in_val - min_in_val) * self.filter_config.edge_filter.cut_off
        out_limit = max_out_val - (max_out_val - min_out_val) * self.filter_config.edge_filter.cut_off
        for i in range(0, sz):
            if in_values[i] >= in_limit:
                self.preserve_mask[i][idx] = True
            if out_values[i] >= out_limit:
                self.preserve_mask[idx][i] = True

    """
    Processes edges of nodes one by one for best edge filter.
    """

    def process_node_edges_best_filter(self, idx):
        # Finding best predecessor and successor of this node
        best_pre = -1
        best_succ = -1
        best_pre_sig = 0.0
        best_succ_sig = 0.0
        sz = self.num_of_nodes
        for i in range(0, sz):
            if i == idx:
                continue
            pre_sig = self.data_repository.binary_weighted_values[i][idx]
            if pre_sig > best_pre_sig:
                best_pre_sig = pre_sig
                best_pre = i
            succ_sig = self.data_repository.binary_weighted_values[idx][i]
            if succ_sig > best_succ_sig:
                best_succ_sig = succ_sig
                best_succ = i
        if best_pre >= 0:
            self.preserve_mask[best_pre][idx] = True
        if best_succ >= 0:
            self.preserve_mask[idx][best_succ] = True

    def apply_node_filter(self, node_filter):
        self.node_filter_resultant_binary_values = self.edge_filter_resultant_binary_values
        self.node_filter_resultant_binary_corr_values = self.edge_filter_resultant_binary_corr_values

    def debug_concurrency_filter_values(self):
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
        pass
