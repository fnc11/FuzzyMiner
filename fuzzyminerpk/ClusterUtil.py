from fuzzyminerpk.FMStructure import FMCluster, FMEdge, FMNode


class ClusterUtil:
    """
    This class's object helps in clusterization process, it provides the functionality needed after node filtering.

    Instance Attributes:
        fm_log_util: holds basic information about the log object\n
        filtered_data_repository: stores data generated by previous filters\n
        node_cluster_mapping: holds the information whether a node is primitive node or assigned to some cluster or
        if it is removed altogether (in case of isolated single node cluster)\n
        cluster_dict: Saves the indices of all primitives nodes inside that cluster, cluster index is used as key\n
        fm_edges_dict: Holds the FMEdge objects, key is pair of node indices (i: source, j: destination)\n
        fm_clusters: Stores the updated list of FMCluster objects.\n
        fm_edges: Used to save final survived edges between clusters and nodes after clusterization process.\n
        fm_nodes: Used to save final survived primitive nodes after clusterization process.\n
    """

    def __init__(self):
        """
        To instantiate the ClusterUtil Object.
        """

        self.fm_log_util = None
        self.filtered_data_repository = None
        self.node_cluster_mapping = list()
        self.cluster_dict = dict()
        self.fm_edges_dict = dict()
        self.fm_clusters = list()
        self.fm_edges = list()
        self.fm_nodes = list()

    def clusterize(self, node_filter, fm_log_util, filtered_data_repository):
        """
        This is main wrapper method which calls different methods needed before, during and after clusterization process

        :param node_filter: new node_filter object to access cut_off value
        :param fm_log_util: basic information about the log object
        :param filtered_data_repository: Filtered Data by Concurrency and Edge filter
        :return: Nothing
        """

        self.fm_log_util = fm_log_util
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
        """
        Clears all lists and dictionary of the ClusterUtil object
        :return: Nothing
        """

        self.node_cluster_mapping = [i for i in range(0, self.fm_log_util.get_num_of_nodes())]
        self.cluster_dict.clear()
        self.fm_edges_dict.clear()
        self.fm_clusters.clear()
        self.fm_nodes.clear()
        self.fm_edges.clear()

    def initialize_clusters(self, cut_off):
        """
        Determines first clusters which are formed from the nodes whose significance is less than given new cut_off.
        While turning normal nodes to clusters it checks if neighbour is already a cluster then it just assigns them to
        the neighbouring cluster otherwise creates a new cluster for that node (victim node). Saves all the newly formed
        clusters in fm_clusters list and also inside cluster_dict (index as their key).
        :param cut_off: New cut_off value according to which clusters should be formed.
        :return: Nothing.
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
        """
        Finds the list of nodes (victims) whose significance value is less than cut_off values.
        :param cut_off: new cut_off value
        :return: list of victim nodes (indices of nodes which didn't survive the new node filter cut_off)
        """

        sz = self.fm_log_util.get_num_of_nodes()
        victims = list()
        for i in range(0, sz):
            if self.filtered_data_repository.node_filter_resultant_unary_values[i] < cut_off:
                victims.append(i)
        return victims

    def get_most_correlated(self, idx):
        """
        Checks the most correlated neighbor of the node according to the binary correlation values.
        :param idx: Index of the node under consideration
        :return: Index of the most correlated neighbor node's index
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
        """
        Checks the preferred merge target of the cluster if it can be merged. There is this special case where we avoid
        merging, that is if there is a primitive node in its predecessors then we don't merge this cluster with any
        predecessor cluster also, same goes with the successors. In case either of them (predecessors and successors)
        contains no primitive node then we find which cluster's primitives are most correlated with this cluster's
        primitives and the winner's index is return. In case both predecessors and successors only contain clusters then
        also the decision is based on their primitive's correlation with the another's primitives.
        :param subject_index: Cluster Index for which preferred merge target is searched.
        :return: Index of the Target if exist or nothing
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
        """
        This method merges the initial clusters generated earlier if they can be merged. During merging all of the
        previous clusters primitives are assigned to the target cluster if any. And the previous cluster is removed
        from the cluster_dict dictionary and fm_clusters list.
        :return: Nothing
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
        """
        Helper method for merge_clusters, it assigns the loser cluster's primitives to winner clusters and changes the
        mapping of primitive nodes of loser cluster to the new winner cluster.
        :param winner_index: Index of the cluster which will devour the other cluster.
        :param loser_index: Index of the cluster which will exist no longer
        :return: Nothing
        """
        loser_primitive_indices = self.cluster_dict[loser_index].get_primitives()
        for prim_idx in loser_primitive_indices:
            self.cluster_dict[winner_index].add_node(prim_idx)
            self.node_cluster_mapping[prim_idx] = winner_index

    def remove_isolated_cluster(self):
        """
        Removes the clusters with no predecessors or successors from the fm_clusters list and cluster_dict dictionary.
        And as the cluster is getting removed it also means that all the primitives will also be removed, basically
        their mapping is set to -1 to indicate that those nodes no longer exist.
        :return: Nothing
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
        """
        Finds all the predecessors of a node.
        :param index: Index of the node
        :return: list of all predecessors of this node
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
        """
        Finds all the successors of a node.
        :param index: Index of the node
        :return: list of all successors of this node
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
        """
        Finds all the predecessors of a cluster by iterating over it's primitives.
        :param index: Index of the cluster
        :return: list of all predecessors of this node
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
        """
        Finds all the successors of a cluster by iterating over it's primitives.
        :param index: Index of the cluster
        :return: list of all successors of this node
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
        """
        Removes singular clusters i.e. cluster with size one and connects its predecessors and successors if needed.
        Removes the cluster from fm_clusters list and cluster_dict dictionary as well.
        :return: Nothing
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
        """
        Calculates collective correlation between two clusters i.e. sum of correlation values between their primitives.
        :param cluster1_idx: Cluster 1 index
        :param cluster2_idx: Cluster 2 index
        :return: Aggregated correlation value
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
        """
        Helper method for remove_singular_cluster, it checks if there's no direct connect between the predecessors and
        successors then it makes one direct connection based on the values gathered from the cluster which is going to
        be removed. Since the cluster supplied is singular cluster means it has only one node, it gets this node's
        predecessors set and successors set, then it checks if there's no relation exist already between those two then
        it calculates the significance and correlation values based on the node (intermediate) which is going to be
        removed and assign that between the nodes from the predecessors and successors set. Basically it makes the
        transitive connection if that doesn't exist already.

        :param cluster: FMCluster object
        :return: Nothing
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
                    self.filtered_data_repository.node_filter_resultant_binary_values[pre_idx][succ_idx] = \
                        (from_sig + to_sig) / 2.0
                    self.filtered_data_repository.node_filter_resultant_binary_corr_values[pre_idx][succ_idx] = \
                        (from_corr + to_corr) / 2.0
                self.filtered_data_repository.node_filter_resultant_binary_values[pre_idx][own_idx] = 0.0
                self.filtered_data_repository.node_filter_resultant_binary_values[own_idx][succ_idx] = 0.0
                self.filtered_data_repository.node_filter_resultant_binary_corr_values[pre_idx][own_idx] = 0.0
                self.filtered_data_repository.node_filter_resultant_binary_corr_values[own_idx][succ_idx] = 0.0
        self.node_cluster_mapping[own_idx] = -1

    def finalize_fm_nodes(self):
        """
        Creates FMNode objects for the primitive nodes which survived the Node Filtering and Clusterization process from
        the node indices and save them in fm_nodes list.
        :return: Nothing
        """

        sz = self.fm_log_util.get_num_of_nodes()
        for i in range(0, sz):
            if self.node_cluster_mapping[i] != -1 and self.node_cluster_mapping[i] < sz:
                self.fm_nodes.append(FMNode(i, self.fm_log_util.nodes[i],
                                            self.filtered_data_repository.node_filter_resultant_unary_values[i]))

    def finalize_fm_edges(self):
        """
        Populates fm_edges_dict dictionary which will be used to generate fm_edges list later. Now during this process
        there are different cases when a edge is stored in this dictionary, please check the different comments in the
        code to understand them.
        :return: Nothing
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
                                        self.fm_edges_dict[(mapped_i, mapped_j)] = FMEdge(mapped_i, mapped_j,
                                                                                          significance, correlation)
        self.populate_fm_edges_from_dict()

    def populate_fm_edges_from_dict(self):
        """
        Fills fm_edges list from the fm_edges_dict dictionary.
        :return: Nothing
        """

        for key, value in self.fm_edges_dict.items():
            self.fm_edges.append(value)

    def finalize_fm_clusters(self):
        """
        Updates the significance values of the clusters depending upon the significance values of its primitive nodes.
        :return: Nothing
        """

        for cluster in self.fm_clusters:
            primitive_indices = cluster.get_primitives()
            primitive_significances = [self.filtered_data_repository.node_filter_resultant_unary_values[idx] for idx in
                                       primitive_indices]
            cluster.significance = sum(primitive_significances) / len(primitive_significances)
