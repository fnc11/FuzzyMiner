from fuzzyminerpk.FMStructure import FMCluster, FMEdge, FMNode


class ClusterUtil:
    def __init__(self):
        self.fm_log_util = None
        self.data_repository = None
        self.filtered_data_repository = None
        self.node_cluster_mapping = list()
        self.cluster_dict = dict()
        self.fm_edges_dict = dict()
        self.fm_clusters = list()
        self.fm_edges = list()
        self.fm_nodes = list()

    def clusterize(self, node_filter, fm_log_util, data_repository, filtered_data_repository):
        # Updated new data
        self.fm_log_util = fm_log_util
        self.data_repository = data_repository
        self.filtered_data_repository = filtered_data_repository

        self.clean_data_storage()
        self.initialize_clusters(node_filter.cut_off)
        self.merge_clusters()
        self.remove_isolated_cluster()
        self.remove_singular_cluster()
        self.finalize_fm_clusters()
        self.finalize_fm_nodes()
        self.finalize_fm_edges()

    def clean_data_storage(self):
        """ Cleans all lists and dictionary of the ClusterUtil object
        """
        self.node_cluster_mapping = [i for i in range(0, self.fm_log_util.get_num_of_nodes())]
        self.cluster_dict.clear()
        self.fm_edges_dict.clear()
        self.fm_clusters.clear()
        self.fm_nodes.clear()
        self.fm_edges.clear()

    def initialize_clusters(self, cut_off):
        """ Initializes victim nodes into clusters
        """

        # list of victim indices
        victims = self.get_victims(cut_off)
        sz = self.fm_log_util.get_num_of_nodes()
        cluster_idx = sz + 1
        for i in range(0, len(victims)):
            if victims[i] == -1:
                continue
            neighbor = self.get_most_correlated(victims[i])
            if neighbor >= sz:
                # if neighbor is a cluster
                self.cluster_dict[neighbor].add_node(victims[i])
                self.node_cluster_mapping[victims[i]] = neighbor
                victims[i] = -1
            else:
                cluster = FMCluster(cluster_idx)
                self.cluster_dict[cluster_idx] = cluster
                # Storing index of the node inside the cluster
                cluster.add_node(victims[i])
                self.node_cluster_mapping[victims[i]] = cluster_idx
                victims[i] = -1
                if neighbor in victims:
                    cluster.add_node(neighbor)
                    self.node_cluster_mapping[neighbor] = cluster_idx
                    victims[victims.index(neighbor)] = -1
                cluster_idx += 1
                # Do we really need fm_clusters list
                self.fm_clusters.append(cluster)

    def get_victims(self, cut_off):
        """ Returns indices of nodes which didn't survive the node filter cut_off
        i.e. needs to be clusterize
        """
        sz = self.fm_log_util.get_num_of_nodes()
        victims = list()
        for i in range(0, sz):
            if self.data_repository.unary_weighted_values[i] < cut_off:
                victims.append(i)
        return victims

    def get_most_correlated(self, idx):
        """ Returns index of most correlated neighbor of the node, takes input as index of the node
        """
        max_corr = 0.0

        # check this initialization
        winner_idx = 0
        sz = self.fm_log_util.get_num_of_nodes()
        for i in range(0, sz):
            if i == idx:
                continue
            # Original code used the data which was available before applying the Edge filter, not sure why
            # maybe it tries to pick best neighbor befor edge_filter remove all connections
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

    def get_preferred_merge_target(self, subject_index):
        """ Returns the target cluster's index from either predecessors or successors,  or None.
        """
        pre_target = None
        succ_target = None
        max_pre_corr = 0.0
        max_succ_corr = 0.0
        sz = self.fm_log_util.get_num_of_nodes()

        # get the indices of all of its predecessors
        pre_decessors = self.get_predecessors_of_cluster(subject_index)
        for pre_decessor in pre_decessors:
            if pre_decessor in self.cluster_dict.keys():
                corr = self.get_aggregate_correlation(subject_index, pre_decessor)
                if corr > max_pre_corr:
                    max_pre_corr = corr
                    pre_target = pre_decessor
            else:
                pre_target = None
                max_pre_corr = 0.0
                break

        successors = self.get_successors_of_cluster(subject_index)
        for successor in successors:
            if successor in self.cluster_dict.keys():
                corr = self.get_aggregate_correlation(subject_index, successor)
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
        """ Iterates over all the clusters and checks if they can be merged
        """

        # Warning code is editing and accessing the same list
        cls_sz = len(self.fm_clusters)
        idx = 0
        while (idx < cls_sz):
            target = self.get_preferred_merge_target(self.fm_clusters[idx].index)
            if target != None:
                self.merge_with(target, self.fm_clusters[idx].index)
                self.cluster_dict.pop(self.fm_clusters[idx].index)
                self.fm_clusters.remove(self.fm_clusters[idx])
                cls_sz -= 1
            else:
                idx += 1

    def merge_with(self, winner_index, loser_index):
        """ Winner cluster devours loser cluster, accepts indices of both the clusters
        """
        loser_primitive_indices = self.cluster_dict[loser_index].get_primitives()
        for prim_idx in loser_primitive_indices:
            self.cluster_dict[winner_index].add_node(prim_idx)
            self.node_cluster_mapping[prim_idx] = winner_index

    def remove_isolated_cluster(self):
        """ Removes clusters with no predecessors or successors from the list.
        """
        cls_sz = len(self.fm_clusters)
        idx = 0
        while idx < cls_sz:
            cluster = self.fm_clusters[idx]
            pre_set = self.get_predecessors_of_cluster(cluster.index)
            succ_set = self.get_successors_of_cluster(cluster.index)
            if len(pre_set) == 0 and len(succ_set) == 0:
                for prim_index in cluster.get_primitives():
                    self.node_cluster_mapping[prim_index] = -1
                self.cluster_dict.pop(cluster.index)
                self.fm_clusters.remove(cluster)
                cls_sz -= 1
            else:
                idx += 1

    def get_predecessors_of_node(self, index):
        """ Returns indices list of the predecessors of a node. Accepts index of the node as input.
        """
        predecessors = set()
        sz = self.fm_log_util.get_num_of_nodes()
        for i in range(0, sz):
            if i == index:
                continue
            elif self.filtered_data_repository.node_filter_resultant_binary_values[i][index] > 0.0:
                if self.node_cluster_mapping[i] != -1:
                    # Puts indices of either simple node or cluster in the set depending upon the mapping
                    predecessors.add(self.node_cluster_mapping[i])
        return predecessors

    def get_successors_of_node(self, index):
        """ Returns indices list of the successors of a node. Accepts index of the node as input.
        """
        successors = set()
        sz = self.fm_log_util.get_num_of_nodes()
        for i in range(0, sz):
            if i == index:
                continue
            elif self.filtered_data_repository.node_filter_resultant_binary_values[index][i] > 0.0:
                if self.node_cluster_mapping[i] != -1:
                    # Puts indices of either simple node or cluster in the set depending upon the mapping
                    successors.add(self.node_cluster_mapping[i])
        return successors

    def get_predecessors_of_cluster(self, index):
        """ Returns a indices list of the predecessors of a cluster. Accepts index of the cluster as input.
        """
        cluster = self.cluster_dict[index]
        predecessors = set()
        for prim_idx in cluster.get_primitives():
            predecessors = predecessors.union(self.get_predecessors_of_node(prim_idx))

        # Remove the primitives from predecessors if any
        predecessors -= set(cluster.get_primitives())

        # Discard the index of cluster itself if included
        predecessors.discard(index)
        return predecessors

    def get_successors_of_cluster(self, index):
        """ Returns a indices list of the successors of a cluster. Accepts index of the cluster as input.
        """
        cluster = self.cluster_dict[index]
        successors = set()
        for prim_idx in cluster.get_primitives():
            successors = successors.union(self.get_successors_of_node(prim_idx))

        # Remove the primitives from successors if any
        successors -= set(cluster.get_primitives())

        # Discard the index of cluster itself if included
        successors.discard(index)
        return successors

    def remove_singular_cluster(self):
        """ Removes singular clusters i.e. cluster with size one and connects its predecessors and successors if needed
        """
        cls_sz = len(self.fm_clusters)
        idx = 0
        while idx < cls_sz:
            cluster = self.fm_clusters[idx]
            if len(cluster.get_primitives()) == 1:
                self.check_for_direct_connection(cluster)
                self.cluster_dict.pop(cluster.index)
                self.fm_clusters.remove(cluster)
                cls_sz -= 1
            else:
                idx += 1

    def get_aggregate_correlation(self, cluster1_idx, cluster2_idx):
        """ Returns collective correlation between two clusters, accepts cluster indices
        """
        cluster1_primitive_indices = self.cluster_dict[cluster1_idx].get_primitives()
        cluster2_primitive_indices = self.cluster_dict[cluster2_idx].get_primitives()
        aggregate_corr = 0.0
        for prim1_idx in cluster1_primitive_indices:
            for prim2_idx in cluster2_primitive_indices:
                aggregate_corr += self.filtered_data_repository.edge_filter_resultant_binary_corr_values[prim1_idx][
                    prim2_idx]
                aggregate_corr += self.filtered_data_repository.edge_filter_resultant_binary_corr_values[prim2_idx][
                    prim1_idx]
        return aggregate_corr

    def check_for_direct_connection(self, cluster):
        """ Checks if there's no direct connect between the predecessors and successors then it makes one directly
        based on the values gathered from the cluster which is going to be removed(in between predecessors and successors)
        """
        node_index = cluster.get_primitives()[0]
        own_idx = node_index
        pre_set = self.get_predecessors_of_node(own_idx)
        succ_set = self.get_successors_of_node(own_idx)
        for pre_idx in pre_set:
            if pre_idx in self.cluster_dict.keys():
                continue
            for succ_idx in succ_set:
                if succ_idx in self.cluster_dict.keys():
                    continue
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

    def finalize_fm_nodes(self):
        """ Creates a list of fm_nodes which survived the Node Filtering and Clusterization process
        """
        sz = self.fm_log_util.get_num_of_nodes()
        for i in range(0, sz):
            if self.node_cluster_mapping[i] != -1 and self.node_cluster_mapping[i] < sz:
                self.fm_nodes.append(FMNode(i, self.fm_log_util.nodes[i], self.data_repository.unary_weighted_values[i]))

    def finalize_fm_edges(self):
        """ Creates an edge dictionary of FMEdges for both FMNodes and FMClusters.
        """
        sz = self.fm_log_util.get_num_of_nodes()
        for i in range(0, sz):
            if self.node_cluster_mapping[i] != -1:
                for j in range(0, sz):
                    significance = self.filtered_data_repository.node_filter_resultant_binary_values[i][j]
                    correlation = self.filtered_data_repository.node_filter_resultant_binary_corr_values[i][j]
                    if significance > 0.0:
                        # Checking if the edge has at least the minimum significance to show in the graph
                        if i == j:
                            # same index will be mapped to same cluster if it is indeed mapped to cluster
                            mapped_idx = self.node_cluster_mapping[i]
                            # Case 1.1 simple nodes are allowed to show self loop if exists
                            if mapped_idx != -1:
                                if mapped_idx < sz:
                                    if (i, j) in self.fm_edges_dict.keys():
                                        if self.fm_edges_dict[(i, j)].significance < significance:
                                            self.fm_edges_dict[(i, j)].significance = significance
                                            self.fm_edges_dict[(i, j)].correlation = correlation
                                    else:
                                        self.fm_edges_dict[(i, j)] = FMEdge(i, j, significance, correlation)
                            # Case 1.2 Cluster nodes no need to show loops, no need to do special handling
                        else:
                            mapped_i = self.node_cluster_mapping[i]
                            mapped_j = self.node_cluster_mapping[j]
                            if mapped_i == -1 or mapped_j == -1:
                                # in case we have removed either of the nodes in clustering process
                                continue
                            else:
                                # Case 2.1 Both single nodes
                                # Case 2.2 Both mapped to different cluster Nodes
                                # Case 2.3 Both mapped to same cluster Nodes ------------> Needs special care
                                # Case 2.4 One Simple and one Cluster

                                if mapped_i == mapped_j:
                                    # Case 2.3
                                    continue
                                else:
                                    # Cases 2.1, 2.2, 2.4
                                    if (mapped_i, mapped_j) in self.fm_edges_dict.keys():
                                        if self.fm_edges_dict[(mapped_i, mapped_j)].significance < significance:
                                            self.fm_edges_dict[(mapped_i, mapped_j)].significance = significance
                                            self.fm_edges_dict[(mapped_i, mapped_j)].correlation = correlation
                                    else:
                                        self.fm_edges_dict[(mapped_i, mapped_j)] = FMEdge(mapped_i, mapped_j, significance, correlation)
        self.populate_fm_edges_from_dict()

    def populate_fm_edges_from_dict(self):
        """ Populates fm_edges list from the fm_edges_dict
        """
        for key, value in self.fm_edges_dict.items():
            self.fm_edges.append(value)

    def finalize_fm_clusters(self):
        for cluster in self.fm_clusters:
            primitive_indices = cluster.get_primitives()
            primitive_significances = [self.data_repository.unary_weighted_values[idx] for idx in primitive_indices]
            cluster.significance = sum(primitive_significances)/len(primitive_significances)