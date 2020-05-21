class FMNode:
    def __init__(self, index, label):
        self.index = index
        self.label = label
        self.pre_list = list()
        self.succ_list = list()


class FMEdge:
    pass


class FMCluster:
    def __init__(self, idx, label=""):
        self.idx = idx
        self.label = label
        self.nodes = list()
        self.pre_list = list()
        self.succ_list = list()

    def add_node(self, node):
        self.nodes.append(node)