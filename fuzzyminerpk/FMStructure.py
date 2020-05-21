class FMNode:
    def __init__(self, index, label, type="primitive"):
        self.index = index
        self.label = label
        self.type = type


class FMEdge:
    def __init__(self, source_index, target_index, significance, correlation):
        self.source = source_index
        self.target = target_index
        self.significance = significance
        self.correlation = correlation


class FMCluster(FMNode):
    def __init__(self, index):
        super().__init__(index, "", "cluster")
        self.label = "cluster" + str(index)
        # this list stores indices of primitive nodes
        self.primitives = list()

    def add_node(self, node_index):
        self.primitives.append(node_index)

    def get_primitives(self):
        return self.primitives
