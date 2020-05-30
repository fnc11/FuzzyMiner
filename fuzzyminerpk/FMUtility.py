import Levenshtein


class FMLogUtils:
    def __init__(self, log):
        self.log = log
        self.nodes = list()
        self.nodes = self.get_nodes()
        self.num_of_nodes = self.get_num_of_nodes()
        self.node_indices = dict()
        self.update_node_index()

    def get_num_of_nodes(self):
        return len(self.nodes)

    def get_nodes(self):
        temp_set = set()
        for trace in self.log:
            for event in trace:
                temp_set.add(event['concept:name'] + "@" + event['lifecycle:transition'])
        return list(temp_set)

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
    # Can use ratio directly but the implementation is not same as fuzzy_miner plugin String Similarity mechanism
    # Levenshtein.ratio(str(first_name), str(second_name))
    # Exact Implementation to Plugin
    dist = Levenshtein.distance(str(first_name), str(second_name))
    big_str_len = max(len(str(first_name)), len(str(second_name)))
    if big_str_len == 0:
        return 1.0
    else:
        return (big_str_len - dist) / big_str_len


def cal_originator_correlation(evt1, evt2):
    first_resource = evt1['org:resource'] if 'org:resource' in evt1 else "<no resource>"
    second_resource = evt2['org:resource'] if 'org:resource' in evt2 else "<no resource>"
    # Can use ratio directly but the implementation is not same as fuzzy_miner plugin String Similarity mechanism
    # return Levenshtein.ratio(str(first_resource), str(second_resource))
    # Exact Implementation to Plugin
    dist = Levenshtein.distance(str(first_resource), str(second_resource))
    big_str_len = max(len(first_resource), len(second_resource))
    if big_str_len == 0:
        return 1.0
    else:
        return (big_str_len - dist) / big_str_len


def cal_datatype_correlation(evt1, evt2):
    ref_data_keys = list()
    fol_data_keys = list()
    for key in evt1:
        if not is_standard_key(key):
            ref_data_keys.append(key)

    for key in evt2:
        if not is_standard_key(key):
            fol_data_keys.append(key)

    if (len(ref_data_keys) == 0) or (len(fol_data_keys) == 0):
        return 0
    overlap = 0
    for key in ref_data_keys:
        if key in fol_data_keys:
            overlap += 1

    return overlap / len(ref_data_keys)


def cal_datavalue_correlation(evt1, evt2):
    ref_data_keys = list()
    fol_data_keys = list()
    for key in evt1:
        if not is_standard_key(key):
            ref_data_keys.append(key)

    for key in evt2:
        if not is_standard_key(key):
            fol_data_keys.append(key)

    if (len(ref_data_keys) == 0) or (len(fol_data_keys) == 0):
        return 0
    key_overlap = 0
    val_overlap = 0
    for key in ref_data_keys:
        if key in fol_data_keys:
            key_overlap += 1
            # Can use ratio directly but the implementation is not same as fuzzy_miner plugin String Similarity mechanism
            # val_overlap += Levenshtein.ratio(str(evt1[key]), str(evt2[key]))
            # Exact Implementation to Plugin
            dist = Levenshtein.distance(str(evt1[key]), str(evt2[key]))
            big_str_len = max(len(str(evt1[key])), len(str(evt2[key])))
            if big_str_len == 0:
                val_overlap += 1.0
            else:
                val_overlap += (big_str_len - dist) / big_str_len

    if key_overlap == 0:
        return 0.0
    else:
        return val_overlap / key_overlap


# To check if values are correct
def is_valid_matrix1D(lst):
    for i in range(0, len(lst)):
        if lst[i] > 0.0:
            return True
    return False


# To check if values are correct
def is_valid_matrix2D(lst):
    for i in range(0, len(lst[0])):
        for j in range(0, len(lst[0])):
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
        norm_list = list()
        for val in lst:
            norm_list.append(val / max_val)
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
        norm_list = list()
        for i in range(0, sz):
            temp_list = list()
            for j in range(0, sz):
                temp_list.append(lst[i][j] / max_val)
            norm_list.append(temp_list)
        return norm_list
