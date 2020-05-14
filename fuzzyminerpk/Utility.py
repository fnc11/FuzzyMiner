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
                temp_set.add(event['concept:name']+"@"+event['lifecycle:transition'])
        return list(temp_set)


def cal_proximity(evt1, evt2):
    # time stamp diff
    pass



def cal_endpoint(evt1, evt2):
    return Levenshtein.ratio(evt1['concept:name'], evt2['concept:name'])


def cal_originator(evt1, evt2):
    # first_resource = evt1['org:resource'] if 'org:resource' in evt1:"<no resource>"
    # second_resource = ev2
    # return Levenshtein.ratio(first_resource, second_resource)
    pass


def cal_datatype(evt1, evt2):
    pass


def cal_datavalue(evt1, evt2):
    pass
