class FMNode:
    def __init__(self, index, label, significance, node_type="primitive"):
        self.index = index
        self.label = label
        self.significance = significance
        self.node_type = node_type

    def __str__(self):
        return self.label+" index: "+str(self.index)+" significance: "+str(self.significance)+" and type: "+self.node_type


class FMEdge:
    def __init__(self, source_index, target_index, significance, correlation):
        self.source = source_index
        self.target = target_index
        self.significance = significance
        self.correlation = correlation

    def __str__(self):
        return "source: "+ str(self.source)+" target: "+str(self.target)+" significance: "+str(self.significance)+" correlation: "+str(self.correlation)


class FMCluster(FMNode):
    def __init__(self, index):
        super().__init__(index, "Cluster", 1.0, "cluster")
        self.primitives = list()

    def add_node(self, node_index):
        self.primitives.append(node_index)

    def get_primitives(self):
        return self.primitives

    def __str__(self):
        return self.label+" index: "+str(self.index)+" mean significance: "+str(self.significance)+" has primitives: "+str(self.get_primitives())
