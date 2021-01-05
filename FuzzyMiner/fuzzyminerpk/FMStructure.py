class FMNode:
    """
    Class for FMNode objects contains all attributes which are necessary for graph drawing.

    Instance Attributes:
        index: index value of the FMNode object
        label: label to show in graph
        significance: significance of this particular object
        node_type: to determine which type of Node it is
    """

    def __init__(self, index, label, significance, node_type="primitive"):
        """
        Instantiates FMNode object
        :param index: index value
        :param label: label
        :param significance: significance of this particular node
        :param node_type: primitives by default
        """

        self.index = index
        self.label = label
        self.significance = significance
        self.node_type = node_type

    def __str__(self):
        return self.label+" index: "+str(self.index)+" significance: "+str(self.significance)+" and type: "+self.node_type


class FMEdge:
    """
    Class for FMEdge objects contains all attributes which are necessary for graph drawing.

    Instance Attributes:
        source: source index of FMNode object
        target_index: destination index of FMNode object
        significance: significance of this edge
        correlation: correlation value of this edge
    """

    def __init__(self, source_index, target_index, significance, correlation):
        """
        Instantiates the FMEdge object.
        :param source_index: source index
        :param target_index: destination index
        :param significance: significance of this edge
        :param correlation: correlation value of this edge
        """

        self.source = source_index
        self.target = target_index
        self.significance = significance
        self.correlation = correlation

    def __str__(self):
        return "source: "+ str(self.source)+" target: "+str(self.target)+" significance: "+str(self.significance)+" correlation: "+str(self.correlation)


class FMCluster(FMNode):
    """
    Class for FMCluster objects extends FMNode, contains one attribute extra, list of primitives.

    Instance Attributes:
        primitives: List of all primitive nodes inside this FMCluster object.
    """
    def __init__(self, index):
        super().__init__(index, "Cluster", 1.0, "cluster")
        self.primitives = list()

    def add_node(self, node_index):
        self.primitives.append(node_index)

    def get_primitives(self):
        return self.primitives

    def __str__(self):
        return self.label+" index: "+str(self.index)+" mean significance: "+str(self.significance)+" has primitives: "+str(self.get_primitives())


class FMMessage:
    """
    Class for FMMessage object, used to send the state of the fuzzy miner process, whether the graph was generated
    successfully or had some issues.

    Instance Attributes:
        message_type: 0: for successful graph generation
                    1: for error while data extraction
                    2: for errors related to metric configurations\n
        message_desc: Short text about the state\n
        graph_path: contains the graph path if it was generated successfully\n
    """

    def __init__(self):
        """
        Instantiates FMMessage object with default values.
        """

        self.message_type = 0
        self.message_desc = "Graph generated successfully"
        self.graph_path = None