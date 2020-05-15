import Levenshtein

from fuzzyminerpk.Utility import FMLogUtils, cal_proximity, cal_endpoint, cal_originator, cal_datatype, cal_datavalue, \
    is_valid_matrix1D, is_valid_matrix2D


class Graph:
    def __init__(self, log, default_config):
        self.config = default_config
        self.fm_log_util = FMLogUtils(log)
        self.log = log
        self.nodes = self.fm_log_util.event_classes()
        self.num_of_nodes = len(self.nodes)
        self.node_indices = dict()
        self.update_node_index()
        # Warning only 20 activities is considered at max
        # self.edges_list = [[0 for x in range(20)] for y in range(20)]
        self.unary_node_frequency_values = [0 for x in range(self.num_of_nodes)]
        self.unary_node_frequency_normalized_values = [0 for x in range(self.num_of_nodes)]

        self.binary_edge_frequency_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_edge_frequency_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_edge_frequency_normalized_values = [[1.0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]

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

        self.extract_dicts()
        
        self.nomalize_primary_metrics()


        ###########Aggregate(simple sum)########
        # unary aggregate computation - used frequency significance, will be used in cal distance
        self.unary_simple_aggregate_values = [0.0 for x in range(self.num_of_nodes)]
        self.unary_simple_aggregate_normalized_values = [0.0 for x in range(self.num_of_nodes)]

        self.cal_unary_simple_aggregate()

        # binary aggregate computation - used frequency significance, will be used in cal routing_significance and distance
        self.binary_simple_aggregate_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_simple_aggregate_normalized_values = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                       range(self.num_of_nodes)]
        self.cal_binary_simple_aggregate()

        # binary aggregate multiple computation - used all binary corr metrics, will be used in cal routing_significance
        self.binary_simple_multi_aggregate_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_simple_multi_aggregate_normalized_values = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                       range(self.num_of_nodes)]
        self.cal_binary_simple_multi_aggregate()

        ###########Derivative metrices######
        self.unary_derivative_routing_values = [0 for x in range(self.num_of_nodes)]
        self.unary_derivative_routing_normalized_values = [0 for x in range(self.num_of_nodes)]

        self.cal_unary_derivate()

        self.binary_derivative_distance_values = [[0 for x in range(self.num_of_nodes)] for y in range(self.num_of_nodes)]
        self.binary_derivative_distance_divisors = [[1.0 for x in range(self.num_of_nodes)] for y in
                                                       range(self.num_of_nodes)]
        self.cal_binary_derivative()

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
        # self.nodes_dict = dict()
        self.node_routing_values = dict()
        self.unary_sig_values = dict()
        # self.cal_unary_metrics()
    
        #binary
        self.edge_distance_values = list()
        self.binary_sig_values = list()
        # self.cal_binary_metrics()
        
        #binary correlation
        self.time_diff_values = list()
        self.resource_corr_values = list()
        self.activity_corr_values = list()
        # self.cal_binary_corr_metrics()


        # binary correlation
        self.time_diff_values = [[0 for x in range(20)] for y in range(20)]
        # initializing with 1 as max disimlar value
        self.resource_corr_values = [[1 for x in range(20)] for y in range(20)]
        self.activity_corr_values = [[1 for x in range(20)] for y in range(20)]
        self.binary_corr_sig_values = [[0 for x in range(20)] for y in range(20)]
        # self.cal_binary_corr_metrics()

        self.clusters = list()
        self.apply_config()

    def extract_dicts(self):
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
                if len(look_back > max_look_back + 1):
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

        # Derivative Metrics
        # cal aggregate values first







        # idx = 0
        # for trace in self.log:
        #     num = len(trace)
        #     for i in range(0, num):
        #         # calculating nodes dictionary
        #         if trace[i]['concept:name'] in self.nodes_dict.keys():
        #             self.nodes_dict[trace[i]['concept:name']] += 1
        #         else:
        #             self.nodes_index[trace[i]['concept:name']] = idx
        #             self.nodes_dict[trace[i]['concept:name']] = 1
        #             idx += 1
        #         #     Add some kind of notifier to the user if activities exceed max num(20 for eg)
        #         # calculating edges 2D matrix
        #         if num > 1 and i > 0:
        #             self.edges_list[self.nodes_index[trace[i - 1]['concept:name']]][
        #                 self.nodes_index[trace[i]['concept:name']]] += 1


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
            in_value, out_value, quotient = 0.0
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

    def nomalize_primary_metrics(self):
        pass


class Cluster:
    pass
