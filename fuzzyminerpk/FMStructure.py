class FMNode:
    def __init__(self, index, label, type="primitive"):
        self.index = index
        self.label = label
        self.type = type
        self.pre_list = list()
        self.succ_list = list()


class FMEdge:
    def __init__(self, source, target, significance, correlation):
        self.source = source
        self.target = target
        self.significance = significance
        self.correlation = correlation


class FMCluster(FMNode):
    def __init__(self, index):
        super().__init__(index, "", "cluster")
        self.label = "cluster" + str(index)
        self.primitives = list()

    def add_node(self, node):
        self.primitives.append(node)