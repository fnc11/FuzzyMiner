import Levenshtein


class FMLogUtils:
    def __init__(self, log):
        self.log = log
        self.nodes = None
        self.num_of_nodes = None
        self.node_indices = None
        self.extract_node_info()

    def get_num_of_nodes(self):
        return len(self.nodes)

    def extract_node_info(self):
        idx = 0
        self.node_indices = dict()
        for trace in self.log:
            for event in trace:
                name = event['concept:name'] + "@" + event['lifecycle:transition']
                if name not in self.node_indices.keys():
                    self.node_indices[name] = idx
                    idx += 1
        self.num_of_nodes = idx
        self.nodes = list(self.node_indices.keys())


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
        time1 = time1.timestamp()*1000
        time2 = time2.timestamp()*1000
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


def is_valid_matrix1D(lst):
    """
    Checks if values are correct
    :param lst: list of elements
    :return: true if all values are non-zero, false otherwise
    """
    for i in range(0, len(lst)):
        if lst[i] > 0.0:
            return True
    return False


def is_valid_matrix2D(dic):
    """
    check if values are correct
    :param dic: dictionary of elements
    :return: true if all values are non-zero, false otherwise
    """
    for i in range(0, len(dic[0])):
        for j in range(0, len(dic[0])):
            if dic[i][j] > 0.0:
                return True
    return False


def normalize_matrix1D(lst):
    max_val = max(lst)
    if max_val == 0:
        return lst
    else:
        norm_list = list()
        for val in lst:
            norm_list.append(val / max_val)
        return norm_list


def normalize_matrix2D(lst):
    sz = len(lst[0])
    max_val = max(map(max, lst))
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


def compensate_frequency(values, divisors):
    sz = len(values[0])
    comp_list = list()
    for i in range(sz):
        temp_list = list()
        for j in range(sz):
            if divisors[i][j] > 0.0:
                temp_list.append(values[i][j] / divisors[i][j])
            else:
                temp_list.append(values[i][j])
        comp_list.append(temp_list)
    return comp_list


def special_weight_normalize2D(values, divisors, invert, normalize_max):
    # This is to compensate frequency, special handling in Prom Plugin
    sz = len(values[0])
    # it is really the weight which is specified for this metric
    if normalize_max == 0:
        norm_list = [[0.0 for i in range(sz)] for j in range(sz)]
        return norm_list
    else:
        comp_list = compensate_frequency(values, divisors)
        max_value = max(map(max, comp_list))
        if max_value > 0.0:
            norm_list = list()
            for i in range(sz):
                temp_list = list()
                for j in range(sz):
                    val = (comp_list[i][j] * normalize_max) / max_value
                    if invert:
                        val = normalize_max - val
                    temp_list.append(val)
                norm_list.append(temp_list)
            return norm_list
        else:
            if invert:
                for i in range(sz):
                    for j in range(sz):
                        comp_list[i][j] = normalize_max - comp_list[i][j]
            return comp_list


def weight_normalize1D(lst, invert, normalize_max):
    sz = len(lst)
    if normalize_max == 0:
        return [0.0 for i in range(sz)]
    else:
        max_val = max(lst)
        if max_val > 0.0:
            norm_list = list()
            for i in range(sz):
                val = (lst[i] * normalize_max) / max_val
                if invert:
                    val = normalize_max - val
                norm_list.append(val)
            return norm_list
        else:
            if invert:
                for i in range(sz):
                    lst[i] = normalize_max - lst[i]
            return lst


def weight_normalize2D(lst, invert, normalize_max):
    sz = len(lst[0])
    if normalize_max == 0:
        return [[0.0 for i in range(sz)] for j in range(sz)]
    else:
        max_val = max(map(max, lst))
        if max_val > 0.0:
            norm_list = list()
            for i in range(sz):
                temp_list = list()
                for j in range(sz):
                    val = (lst[i][j] * normalize_max) / max_val
                    if invert:
                        val = normalize_max - val
                    temp_list.append(val)
                norm_list.append(temp_list)
            return norm_list
        else:
            if invert:
                for i in range(sz):
                    for j in range(sz):
                        lst[i][j] = normalize_max - lst[i][j]
            return lst
