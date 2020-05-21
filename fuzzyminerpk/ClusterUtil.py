from fuzzyminerpk.FMStructure import FMCluster, FMEdge, FMNode


class ClusterUtil:
    def __init__(self, fm_log_util, data_repository, filtered_data_repository):
        self.fm_log_util = fm_log_util
        self.data_repository = data_repository
        self.filtered_data_repository = filtered_data_repository
        self.node_cluster_mapping = [i for i in range(0, self.fm_log_util.get_num_of_nodes())]
        self.cluster_dict = dict()
        self.clusters = list()
        self.fm_edges_dict = dict()
        self.fm_nodes = list()

    def clusterize(self, node_filter):
        self.clean_data_storage()
        self.initialize_clusters(node_filter)
        self.merge_clusters()
        self.remove_isolated_cluster()
        self.create_simple_fm_nodes()
        self.finalize_edges()

    def initialize_clusters(self, node_filter):
        victims = self.get_victims(node_filter.cut_off)
        cluster_idx = self.fm_log_util.get_num_of_nodes() + 1
        sz = self.fm_log_util.get_num_of_nodes()
        for i in range(0, len(victims)):
            neighbor = self.get_most_correlated(victims[i])
            if neighbor >= sz:
                self.cluster_dict[neighbor].add_node(self.fm_log_util.nodes[victims[i]])
                self.node_cluster_mapping[victims[i]] = neighbor
                victims[i] = -1
            else:
                cluster = FMCluster(cluster_idx)
                self.cluster_dict[cluster_idx] = cluster
                # Check if necessary to store entire node object
                cluster.add_node(self.fm_log_util.nodes[victims[i]])
                self.node_cluster_mapping[victims[i]] = cluster_idx
                cluster_idx += 1
                victims[i] = -1
                if neighbor in victims:
                    cluster.add_node(self.fm_log_util.nodes[neighbor])
                    self.node_cluster_mapping[neighbor] = cluster_idx
                    victims[victims.index(neighbor)] = -1
                self.clusters.append(cluster)

    def get_victims(self, cut_off):
        sz = self.fm_log_util.get_num_of_nodes()
        victims = list()
        for i in range(0, sz):
            if self.data_repository.unary_weighted_values[i] < cut_off:
                victims.append(i)
        return victims

    def get_most_correlated(self, idx):
        max_corr = 0.0
        # check this initialization
        winner_idx = 0
        sz = self.fm_log_util.get_num_of_nodes()
        for i in range(0, sz):
            if i == idx:
                continue
            # Original code used the data which was available before applying the Edge filter
            curr_corr = self.filtered_data_repository.concurrency_filter_resultant_binary_corr_values[idx][i]
            if curr_corr > max_corr:
                # Returns index of cluster or node(if it hasn't become one)
                winner_idx = self.node_cluster_mapping[i]
                max_corr = curr_corr
            curr_corr = self.filtered_data_repository.concurrency_filter_resultant_binary_corr_values[i][idx]
            if curr_corr > max_corr:
                winner_idx = self.node_cluster_mapping[i]
                max_corr = curr_corr
        return winner_idx

    def get_preferred_merge_target(self, subject):
        pre_target = None
        succ_target = None
        max_pre_corr = 0.0
        max_succ_corr = 0.0
        sz = self.fm_log_util.get_num_of_nodes()
        pre_decessors = subject.get_predecessors()
        for pre_decessor in pre_decessors:
            if pre_decessor.index in self.cluster_dict.keys():
                corr = self.get_aggregate_correlation(subject, pre_decessor)
                if corr > max_pre_corr:
                    max_pre_corr = corr
                    pre_target = pre_decessor
            else:
                pre_target = None
                max_pre_corr = 0.0
                break

        successors = subject.get_successors()
        for successor in successors:
            if successor.index in self.cluster_dict.keys():
                corr = self.get_aggregate_correlation(subject, successor)
                if corr > max_succ_corr:
                    max_succ_corr = corr
                    succ_target = successor
            else:
                if pre_target != None:
                    return pre_target
                else:
                    return None

        if max_pre_corr > max_succ_corr:
            return pre_target
        else:
            return succ_target

    def merge_clusters(self):
        # Warning code is editing and accessing the same list
        cls_sz = len(self.clusters)
        idx = 0
        while (idx < cls_sz):
            target = self.get_preferred_merge_target(self.clusters[idx])
            if target != None:
                self.merge_with(target, self.clusters[idx])
                self.clusters.remove(self.clusters[idx])
                cls_sz -= 1
            else:
                idx += 1

    def merge_with(self, winner, loser):
        loser_primitives = loser.get_primitives()
        for prim in loser_primitives:
            winner.add(prim)
            self.node_cluster_mapping[prim.index] = winner.index
        self.cluster_dict.pop(loser.index)
        self.clusters.remove(loser)

    def remove_isolated_cluster(self):
        cls_sz = len(self.clusters)
        idx = 0
        while idx < cls_sz:
            cluster = self.clusters[idx]
            pre_set = cluster.get_predecessors()
            succ_set = cluster.get_successors()
            if len(pre_set) == 0 and len(succ_set) == 0:
                for prim in cluster.get_primitives():
                    self.node_cluster_mapping[prim.index] = -1
                self.cluster_dict.pop(cluster.index)
                self.clusters.remove(cluster)
                cls_sz -= 1
            else:
                idx += 1

    def remove_singular_cluster(self, graph, clusters):
        cls_sz = len(self.clusters)
        idx = 0
        while idx < cls_sz:
            cluster = self.clusters[idx]
            if len(cluster.get_primitives()) == 1:
                self.check_for_direct_connection(cluster)
                self.cluster_dict.pop(cluster.index)
                self.clusters.remove(cluster)
                cls_sz -= 1
            else:
                idx += 1

    # Used to clean all lists and dicts
    def clean_data_storage(self):
        pass

    def get_aggregate_correlation(self, cluster1, cluster2):
        cluster1_primitives = cluster1.get_primitives()
        cluster2_primitives = cluster2.get_primitives()
        aggregate_corr = 0.0
        for prim_a in cluster1_primitives:
            for prim_b in cluster2_primitives:
                aggregate_corr += self.filtered_data_repository.edge_filter_resultant_binary_corr_values[prim_a.index][
                    prim_b.index]
                aggregate_corr += self.filtered_data_repository.edge_filter_resultant_binary_corr_values[prim_b.index][
                    prim_a.index]
        return aggregate_corr

    def check_for_direct_connection(self, cluster):
        node = cluster.get_primitives()[0]
        own_idx = node.index
        pre_set = node.get_predecessors()
        succ_set = node.get_successors()
        for pre_entity in pre_set:
            if pre_entity in self.clusters:
                continue
            pre_idx = pre_entity.index
            for succ_entity in succ_set:
                if succ_entity in self.clusters:
                    continue
                succ_idx = succ_entity.index
                if self.filtered_data_repository.edge_filter_resultant_binary_values[pre_idx][succ_idx] == 0.0:
                    from_sig = self.filtered_data_repository.edge_filter_resultant_binary_values[pre_idx][own_idx]
                    to_sig = self.filtered_data_repository.edge_filter_resultant_binary_values[own_idx][succ_idx]
                    from_corr = self.filtered_data_repository.edge_filter_resultant_binary_corr_values[pre_idx][own_idx]
                    to_corr = self.filtered_data_repository.edge_filter_resultant_binary_corr_values[own_idx][succ_idx]
                    # Store in new copy of resultant values
                    self.filtered_data_repository.node_filter_resultant_binary_values[pre_idx][succ_idx] = (
                                                                                                                       from_sig + to_sig) / 2.0
                    self.filtered_data_repository.node_filter_resultant_binary_corr_values[pre_idx][succ_idx] = (
                                                                                                                            from_corr + to_corr) / 2.0
                self.filtered_data_repository.node_filter_resultant_binary_values[pre_idx][own_idx] = 0.0
                self.filtered_data_repository.node_filter_resultant_binary_values[own_idx][succ_idx] = 0.0
                self.filtered_data_repository.node_filter_resultant_binary_corr_values[pre_idx][own_idx] = 0.0
                self.filtered_data_repository.node_filter_resultant_binary_corr_values[own_idx][succ_idx] = 0.0
        self.node_cluster_mapping[own_idx] = -1
        self.cluster_dict.pop(cluster.index)
        self.clusters.remove(cluster)

    def create_simple_fm_nodes(self):
        sz = self.fm_log_util.get_num_of_nodes()
        for i in range(0, sz):
            if self.node_cluster_mapping[i] != -1:
                self.fm_nodes.append(FMNode(i, self.fm_log_util.nodes[i]))

    def finalize_edges(self):
        sz = self.fm_log_util.get_num_of_nodes()
        for i in range(0, sz):
            if self.node_cluster_mapping[i] != -1:
                for j in range(0, sz):
                    if self.node_cluster_mapping[j] != -1:
                        mapped_i = self.node_cluster_mapping[i]
                        mapped_j = self.node_cluster_mapping[j]
                        significance = self.filtered_data_repository.node_filter_resultant_binary_values[i][j]
                        correlation = self.filtered_data_repository.node_filter_resultant_binary_corr_values[i][j]
                        # There'll be multiple cases
                        # Case 1. Either mapping to same cluster or it is same simple node, in case of cluster nothing to do
                        if i == j and mapped_i < sz:
                            # Case 1.1 same simple node
                            if self.filtered_data_repository.node_filter_resultant_binary_values[i][j] > 0.001:
                                if (i, j) in self.fm_edges_dict.keys():
                                    if self.fm_edges_dict[(i, j)].significane > significance:
                                        self.fm_edges_dict[(i, j)].significance = significance
                                        self.fm_edges_dict[(i, j)].correlation = correlation
                                else:
                                    self.fm_edges_dict[(i, j)] = FMEdge(i, j, significance, correlation)
                        elif mapped_i < sz and mapped_j < sz:
                            # Case 2. Both are simple nodes
                            if (i, j) in self.fm_edges_dict.keys():
                                if self.fm_edges_dict[(i, j)].significane > significance:
                                    self.fm_edges_dict[(i, j)].significance = significance
                                    self.fm_edges_dict[(i, j)].correlation = correlation
                            else:
                                self.fm_edges_dict[(i, j)] = FMEdge(i, j, significance, correlation)
                        else:
                            # Case 3. One or both are clusters
                            if mapped_i > sz and mapped_j > sz:
                                # Case 3.1 Both are clusters
                                if (mapped_i, mapped_j) in self.fm_edges_dict.keys():
                                    if self.fm_edges_dict[(mapped_i, mapped_j)].significane > significance:
                                        self.fm_edges_dict[(mapped_i, mapped_j)].significance = significance
                                        self.fm_edges_dict[(mapped_i, mapped_j)].correlation = correlation
                                else:
                                    self.fm_edges_dict[(mapped_i, mapped_j)] = FMEdge(mapped_i, mapped_j, significance,
                                                                                      correlation)
                            elif mapped_i < sz:
                                # Case 3.2 First is simple node, 2nd is cluster
                                if (i, mapped_j) in self.fm_edges_dict.keys():
                                    if self.fm_edges_dict[(i, mapped_j)].significane > significance:
                                        self.fm_edges_dict[(i, mapped_j)].significance = significance
                                        self.fm_edges_dict[(i, mapped_j)].correlation = correlation
                                else:
                                    self.fm_edges_dict[(i, mapped_j)] = FMEdge(i, mapped_j, significance, correlation)
                            else:
                                # Case 3.3 First is cluster and 2nd is simple node
                                if (mapped_i, j) in self.fm_edges_dict.keys():
                                    if self.fm_edges_dict[(mapped_i, j)].significane > significance:
                                        self.fm_edges_dict[(mapped_i, j)].significance = significance
                                        self.fm_edges_dict[(mapped_i, j)].correlation = correlation
                                else:
                                    self.fm_edges_dict[(mapped_i, j)] = FMEdge(mapped_i, j, significance, correlation)
