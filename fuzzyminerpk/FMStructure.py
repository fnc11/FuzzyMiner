class FMNode:
    def __init__(self, index, label, type="primitive"):
        self.index = index
        self.label = label + str(index)
        self.type = type

    def __repr__(self):
        print(self.label+" and type: "+self.type)


class FMEdge:
    def __init__(self, source_index, target_index, significance, correlation):
        self.source = source_index
        self.target = target_index
        self.significance = significance
        self.correlation = correlation

    def __repr__(self):
        print("source: "+ str(self.source)+" target: "+str(self.target)+" significance: "+str(self.significance)+" correlation: "+str(self.correlation))


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

    def __repr__(self):
        print(self.label+" has primitives: "+str(self.get_primitives()))
