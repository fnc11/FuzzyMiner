import Levenshtein


class FMLogUtils:
    def __init__(self, log):
        self.log = log
        self.num_of_event_classes = 0
        self.event_classes = list()

    def get_num_of_event_classes(self):
        if self.num_of_event_classes == 0:
            self.event_classes = self.get_event_classes()
        return len(self.event_classes)

    def get_event_classes(self):
        temp_set = set()
        for trace in self.log:
            for event in trace:
                temp_set.add(event['concept:name'] + "@" + event['lifecycle:transition'])
        return list(temp_set)


def is_standard_key(key):
    if key == "concept" or key == "lifecycle" or key == "org" or key == "time" or key == "semantic":
        return True
    else:
        return False


def cal_proximity(evt1, evt2):
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


def cal_endpoint(evt1, evt2):
    first_name = evt1['concept:name'] if 'concept:name' in evt1 else "<no name>"
    second_name = evt2['concept:name'] if 'concept:name' in evt2 else "<no name>"
    return Levenshtein.ratio(first_name, second_name)


def cal_originator(evt1, evt2):
    first_resource = evt1['org:resource'] if 'org:resource' in evt1 else "<no resource>"
    second_resource = evt2['org:resource'] if 'org:resource' in evt2 else "<no resource>"
    return Levenshtein.ratio(first_resource, second_resource)


def cal_datatype(evt1, evt2):
    ref_data_key_set = list()
    fol_data_key_set = list()
    for key in evt1:
        if not is_standard_key(key):
            ref_data_key_set.append(key)

    for key in evt2:
        if not is_standard_key(key):
            fol_data_key_set.append(key)

    if (len(ref_data_key_set) == 0) or (len(fol_data_key_set) == 0):
        return 0
    overlap = 0
    for i in ref_data_key_set:
        for j in fol_data_key_set:
            if ref_data_key_set[i] == fol_data_key_set[j]:
                overlap += 1

    return overlap / len(ref_data_key_set)


def cal_datavalue(evt1, evt2):
    ref_data_key_set = list()
    fol_data_key_set = list()
    for key in evt1:
        if not is_standard_key(key):
            ref_data_key_set.append(key)

    for key in evt2:
        if not is_standard_key(key):
            fol_data_key_set.append(key)

    if (len(ref_data_key_set) == 0) or (len(fol_data_key_set) == 0):
        return 0
    key_overlap = 0
    val_overlap = 0
    for key in ref_data_key_set:
        if key in fol_data_key_set:
            key_overlap += 1
            val_overlap += Levenshtein.ratio(evt1[key], evt2[key])

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
    maxFound = 0.0
    for col in range(len(lst), 0, -1):
        for row in (len(lst), 0, -1):
            current = lst[col][row]
            if current > maxFound:
                maxFound = current
    if maxFound > 0:
        return True
    else:
        return False
