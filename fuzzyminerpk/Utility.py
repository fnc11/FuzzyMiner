from datetime import datetime

import Levenshtein
import numpy as np


class FMLogUtils:
    def __init__(self, log):
        self.log = log
        # self.nodes = list()
        self.nodes = np.empty(0)
        self.nodes = self.get_nodes()
        self.num_of_nodes = self.get_num_of_nodes()
        self.node_indices = dict()
        self.update_node_index()

    def get_num_of_nodes(self):
        sz = np.size(self.nodes)
        return sz

    def get_nodes(self):
        temp_set = set()
        for trace in self.log:
            for event in trace:
                temp_set.add(event['concept:name'] + "@" + event['lifecycle:transition'])
        return np.asarray(list(temp_set))


    """
    This populates the node_indices dictionary from the event classes;
    """
    def update_node_index(self):
        idx = 0
        for node in self.nodes:
            self.node_indices[node] = idx
            idx += 1


def is_standard_key(key):
    if key.find("concept") != -1 or key.find("lifecycle") != -1 or key.find("org") != -1 or key.find(
            "time") != -1 or key.find("semantic") != -1:
        return True
    else:
        return False


def cal_proximity_correlation(evt1, evt2):
    if 'time:timestamp' not in evt1 or 'time:timestamp' not in evt2:
        return 0.0
    time1 = evt1['time:timestamp']
    time2 = evt2['time:timestamp']
    if time1 is not None and time2 is not None:
        time1 = time1.timestamp()
        time2 = time2.timestamp()
        if time1 != time2:
            return 1.0 / (time2 - time1)
        else:
            return 1.0
    else:
        return 0.0


def cal_endpoint_correlation(evt1, evt2):
    first_name = evt1['concept:name'] if 'concept:name' in evt1 else "<no name>"
    second_name = evt2['concept:name'] if 'concept:name' in evt2 else "<no name>"
    # Note this implementation is not same as fuzzy_miner plugin String Similarity mechanism
    return Levenshtein.ratio(str(first_name), str(second_name))


def cal_originator_correlation(evt1, evt2):
    first_resource = evt1['org:resource'] if 'org:resource' in evt1 else "<no resource>"
    second_resource = evt2['org:resource'] if 'org:resource' in evt2 else "<no resource>"
    # Note this implementation is not same as fuzzy_miner plugin String Similarity mechanism
    return Levenshtein.ratio(str(first_resource), str(second_resource))


def cal_datatype_correlation(evt1, evt2):
    # ref_data_keys = list()
    ref_data_keys = np.empty(0)
    # fol_data_keys = list()
    fol_data_keys = np.empty(0)
    for key in evt1:
        if not is_standard_key(key):
            ref_data_keys = np.append(ref_data_keys, key)

    for key in evt2:
        if not is_standard_key(key):
            fol_data_keys = np.append(fol_data_keys, key)

    if (np.size(ref_data_keys) == 0) or (np.size(fol_data_keys) == 0):
        return 0
    overlap = 0
    for key1 in ref_data_keys:
        for key2 in fol_data_keys:
            if key1 == key2:
                overlap += 1

    return overlap / len(ref_data_keys)


def cal_datavalue_correlation(evt1, evt2):
    # ref_data_keys = list()
    ref_data_keys = np.empty(0)
    # fol_data_keys = list()
    fol_data_keys = np.empty(0)
    for key in evt1:
        if not is_standard_key(key):
            ref_data_keys = np.append(ref_data_keys, key)

    for key in evt2:
        if not is_standard_key(key):
            fol_data_keys = np.append(fol_data_keys, key)

    if (np.size(ref_data_keys) == 0) or (np.size(fol_data_keys) == 0):
        return 0
    key_overlap = 0
    val_overlap = 0
    for key in ref_data_keys:
        if key in fol_data_keys:
            key_overlap += 1
            val_overlap += Levenshtein.ratio(str(evt1[key]), str(evt2[key]))
            # Note this implementation is not same as fuzzy_miner plugin String Similarity mechanism

    if key_overlap == 0:
        return 0.0
    else:
        return val_overlap / key_overlap


# To check if values are correct
def is_valid_matrix1D(lst):
    for i in range(0, np.size(lst)):
        if lst[i] > 0.0:
            return True
    return False


# To check if values are correct
def is_valid_matrix2D(lst):
    for i in range(0, np.size(lst[0])):
        for j in range(0, np.size(lst[0])):
            if lst[i][j] > 0.0:
                return True
    return False

def normalize_matrix1D(lst):
    max_val = 0
    for val in lst:
        if val > max_val:
            max_val = val
    if max_val == 0:
        return lst
    else:
        # norm_list = list()
        norm_list = np.empty(0)
        for val in lst:
            norm_list = np.append(norm_list, (val / max_val))
        return norm_list


def normalize_matrix2D(lst):
    max_val = 0
    sz = len(lst[0])
    for i in range(0, sz):
        for j in range(0, sz):
            if lst[i][j] > max_val:
                max_val = lst[i][j]
    if max_val == 0:
        return lst
    else:
        # norm_list = list()
        norm_list = np.empty(0)
        for i in range(0, sz):
            temp_list = np.empty(0)
            for j in range(0, sz):
                temp_list = np.append(temp_list, (lst[i][j] / max_val))
            norm_list = np.append(norm_list, temp_list)
        return norm_list
