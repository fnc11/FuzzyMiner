from fuzzyminerpk.Utility import FMLogUtils, cal_proximity, cal_endpoint, cal_originator, cal_datatype, cal_datavalue, \
    is_valid_matrix2D, is_valid_matrix1D, normalize_matrix1D, normalize_matrix2D


class DataRepository:
    def __init__(self, log, config):
        self.log = log
        self.config = config
        self.fm_log_util = FMLogUtils(log)
        self.node_indices = dict()
        self.nodes = self.fm_log_util.get_event_classes()
        self.num_of_nodes = len(self.nodes)
        self.update_node_index()
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
        self.unary_simple_aggregate_values = list()
        self.unary_simple_aggregate_normalized_values = list()
        # binary aggregate computation - used frequency significance, will be used in cal routing_significance and distance
        self.binary_simple_aggregate_values = list()
        self.binary_simple_aggregate_normalized_values = list()
        # binary aggregate multiple computation - used all binary corr metrics, will be used in cal routing_significance
        self.binary_simple_multi_aggregate_values = list()
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
        # extract data from log

    def init_lists(self):
        self.unary_node_frequency_values = [0 for x in range(self.num_of_nodes)]
        self.unary_node_frequency_normalized_values = [0 for x in range(self.num_of_nodes)]

        self.binary_edge_frequency_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_edge_frequency_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                               range(self.num_of_nodes)]
        self.binary_edge_frequency_normalized_values = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                        range(self.num_of_nodes)]

        self.binary_corr_proximity_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_corr_proximity_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                               range(self.num_of_nodes)]
        self.binary_corr_proximity_normalized_values = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                        range(self.num_of_nodes)]

        self.binary_corr_endpoint_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_corr_endpoint_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                              range(self.num_of_nodes)]
        self.binary_corr_endpoint_normalized_values = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                       range(self.num_of_nodes)]

        self.binary_corr_originator_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_corr_originator_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                range(self.num_of_nodes)]
        self.binary_corr_originator_normalized_values = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                         range(self.num_of_nodes)]

        self.binary_corr_datatype_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_corr_datatype_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                              range(self.num_of_nodes)]
        self.binary_corr_datatype_normalized_values = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                       range(self.num_of_nodes)]

        self.binary_corr_datavalue_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_corr_datavalue_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                               range(self.num_of_nodes)]
        self.binary_corr_datavalue_normalized_values = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                        range(self.num_of_nodes)]

        ###########Aggregate(simple sum)########
        # unary aggregate computation - used frequency significance, will be used in cal distance
        self.unary_simple_aggregate_values = [0.0 for x in range(self.num_of_nodes)]
        self.unary_simple_aggregate_normalized_values = [0.0 for x in range(self.num_of_nodes)]


        # binary aggregate computation - used frequency significance, will be used in cal routing_significance and distance
        self.binary_simple_aggregate_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_simple_aggregate_normalized_values = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                          range(self.num_of_nodes)]

        # binary aggregate multiple computation - used all binary corr metrics, will be used in cal routing_significance
        self.binary_simple_multi_aggregate_values = [[0 for x in range(self.num_of_nodes)] for y in
                                                     range(self.num_of_nodes)]
        self.binary_simple_multi_aggregate_normalized_values = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                                range(self.num_of_nodes)]

        ###########Derivative metrices######
        self.unary_derivative_routing_values = [0 for x in range(self.num_of_nodes)]
        self.unary_derivative_routing_normalized_values = [0 for x in range(self.num_of_nodes)]


        self.binary_derivative_distance_values = [[0 for x in range(self.num_of_nodes)] for y in
                                                  range(self.num_of_nodes)]
        self.binary_derivative_distance_normalized_values = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                    range(self.num_of_nodes)]

        ########Weighted lists###########
        self.unary_weighted_values = [0 for x in range(self.num_of_nodes)]
        self.binary_weighted_values = [[0 for x in range(self.num_of_nodes)] for y in
                                                  range(self.num_of_nodes)]
        self.binary_corr_weighted_values = [[0 for x in range(self.num_of_nodes)] for y in
                                                  range(self.num_of_nodes)]


    def extract_primary_metrics(self):
        max_look_back = self.config.chunk_size
        for trace in self.log:
            look_back = list()
            look_back_indices = list()
            for event in trace:
                follower_event = event
                follower_index = self.node_indices[follower_event['concept:name']+"@"+follower_event['lifecycle:transition']]
                look_back.insert(0, follower_event)
                look_back_indices.insert(0, follower_index)
                # check to remove extra elements from the list
                # check for out of index error
                if len(look_back) > max_look_back + 1:
                    look_back.pop(max_look_back+1)
                    look_back_indices.pop(max_look_back+1)
                # Calculating unary frequency values for the nodes
                self.unary_node_frequency_values[follower_index] = 1
                # Iterating over multi-step relations
                for k in range(1, len(look_back)):
                    ref_event = look_back[k]
                    ref_index = look_back_indices[k]

                    att_factor = self.config.attenuation.get_attenuation_factor(k)

                    # 1 Edge frequency metric
                    self.binary_edge_frequency_values[ref_index][follower_index] += 1.0 * att_factor
                    self.binary_edge_frequency_divisors[ref_index][follower_index] += att_factor

                    # 2 Proximity calculation
                    self.binary_corr_proximity_values[ref_index][follower_index] += cal_proximity(ref_event, follower_event)*att_factor
                    self.binary_corr_proximity_divisors[ref_index][follower_index] += att_factor

                    # 3 End Point calculation
                    self.binary_corr_endpoint_values[ref_index][follower_index] += cal_endpoint(ref_event, follower_event)*att_factor
                    self.binary_corr_endpoint_divisors[ref_index][follower_index] += att_factor

                    # 4 Originator calculation
                    self.binary_corr_originator_values[ref_index][follower_index] += cal_originator(ref_event, follower_event)*att_factor
                    self.binary_corr_originator_divisors[ref_index][follower_index] += att_factor

                    # 5 DataType calculation
                    self.binary_corr_datatype_values[ref_index][follower_index] += cal_datatype(ref_event, follower_event)*att_factor
                    self.binary_corr_datatype_divisors[ref_index][follower_index] += att_factor

                    # 6 DataValue calculation
                    self.binary_corr_datavalue_values[ref_index][follower_index] += cal_datavalue(ref_event, follower_event)*att_factor
                    self.binary_corr_datavalue_divisors[ref_index][follower_index] += att_factor

    def extract_simple_aggregates(self):
        self.cal_unary_simple_aggregate()
        self.cal_binary_simple_aggregate()
        self.cal_binary_simple_multi_aggregate()

    def extract_derivative_metrics(self):
        self.cal_unary_derivate()
        self.cal_binary_derivative()

    """
    To extract weighted from the normalized metrics according to their weight into three separate lists
    """
    def extract_weighted_metrics(self):
        pass

    def cal_unary_simple_aggregate(self):
        ## Caution Use normalized value of all the metrics
        if is_valid_matrix1D(self.unary_node_frequency_values):
            ##Caution for this zero value
            temp_max = 0.0
            for i in range(0, len(self.unary_node_frequency_values)):
                self.unary_simple_aggregate_values[i] = self.unary_node_frequency_values[i]
                if self.unary_node_frequency_values[i] > temp_max:
                    temp_max = self.unary_node_frequency_values[i]
            for i in range(0, len(self.unary_node_frequency_values)):
                # Note: Could also fill normalized list self.binary_edge_frequency_normalized_values
                self.unary_simple_aggregate_normalized_values[i] *= (1/temp_max)
        else:
            ##Caution: Check if we need to return or do somthing else
            return

    def cal_binary_simple_aggregate(self):
        ## Caution Use normalized value of all the metrics
        if is_valid_matrix2D(self.binary_edge_frequency_values):
            ##Caution for this zero value
            temp_max = 0.0
            sz = len(self.binary_edge_frequency_values)
            for i in range(0, sz):
                for j in range(0, sz):
                    self.binary_simple_aggregate_values[i][j] = self.binary_edge_frequency_values[i][j]
                    if self.binary_edge_frequency_values[i][j] > temp_max:
                        temp_max = self.binary_edge_frequency_values[i][j]
            for i in range(0, sz):
                for j in range(0, sz):
                    # Note: Could also fill normalized list self.binary_edge_frequency_normalized_values
                    self.binary_simple_aggregate_values[i][j] *= (1/temp_max)
        else:
            ##Caution: Check if we need to return or do somthing else
            return

    def cal_binary_simple_multi_aggregate(self):
        #Will be used for correlating related metric aggregation
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
        temp_max = 0.0
        if len(valid_metrics) > 0:
            sz = self.num_of_nodes
            for i in range(0, sz):
                for j in range(0, sz):
                    aggregated = 0.0
                    for k in range(0, len(valid_metrics)):
                        # Check if this below code is accessing values correctly
                        aggregated += valid_metrics[k][i][j]

                    self.binary_simple_multi_aggregate_values[i][j] = aggregated
                    if aggregated > temp_max:
                        temp_max = aggregated
            for i in range(0, sz):
                for j in range(0, sz):
                    self.binary_simple_multi_aggregate_normalized_values[i][j] *= (1/temp_max)
        else:
            ##Caution: Check if we need to return or do somthing else
            return

    def cal_unary_derivate(self):
        sz = self.num_of_nodes
        for i in range(0, sz):
            in_value = 0.0
            out_value = 0.0
            quotient = 0.0
            for x in range(0, sz):
                if x == i:
                    continue
                in_value += self.binary_simple_aggregate_normalized_values[x][i]*self.binary_simple_multi_aggregate_normalized_values[x][i]
                out_value += self.binary_simple_aggregate_normalized_values[i][x] * \
                           self.binary_simple_multi_aggregate_normalized_values[i][x]
            if in_value == 0.0 and out_value == 0.0:
                quotient = 0.0
            else:
                quotient = abs((in_value - out_value)/(in_value + out_value))
            self.unary_derivative_routing_values[i] = quotient

    def cal_binary_derivative(self):
        sz = self.num_of_nodes
        for i in range(0, sz):
            sig_source = self.unary_simple_aggregate_normalized_values[i]
            for j in range(0, sz):
                sig_target = self.unary_simple_aggregate_normalized_values[j]
                sig_link = self.binary_simple_aggregate_normalized_values[i][j]
                self.binary_derivative_distance_values[i][j] = 1.0 - ((sig_source - sig_link) + (sig_target - sig_link)) / (sig_source + sig_target)

    def normalize_primary_metrics(self):
        self.unary_node_frequency_normalized_values = normalize_matrix1D(self.unary_node_frequency_values)
        self.binary_edge_frequency_normalized_values = normalize_matrix2D(self.binary_edge_frequency_values)
        self.binary_corr_proximity_normalized_values = normalize_matrix2D(self.binary_corr_proximity_values)
        self.binary_corr_endpoint_normalized_values = normalize_matrix2D(self.binary_corr_endpoint_values)
        self.binary_corr_originator_normalized_values = normalize_matrix2D(self.binary_corr_originator_values)
        self.binary_corr_datatype_normalized_values = normalize_matrix2D(self.binary_corr_datatype_values)
        self.binary_corr_datavalue_normalized_values = normalize_matrix2D(self.binary_corr_datavalue_values)

    def normalize_derivative_metrics(self):
        self.unary_derivative_routing_normalized_values = normalize_matrix1D(self.unary_derivative_routing_values)
        self.binary_derivative_distance_normalized_values = normalize_matrix2D(self.binary_derivative_distance_values)

    def update_node_index(self):
        idx = 0
        for node in self.nodes:
            self.node_indices[node] = idx
            idx += 1