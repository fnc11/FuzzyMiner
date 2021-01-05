class Filter:
    """
    Base class for all filter objects.

    Instance Attributes:
        name: name of the filter
    """

    def __init__(self, name):
        """
        Instantiates the filter object.
        :param name: name of the filter
        """

        self.name = name

    def __str__(self):
        return "Filter name: " + self.name


class NodeFilter(Filter):
    """
    Class for NodeFilter objects, extends Filter class.

    Instance Attributes:
        cut_off: cut_off value of the node filter.
    """

    def __init__(self, cut_off=0.0):
        """
        Instantiates NodeFilter object
        :param cut_off: cut_off, default is 0.0
        """

        super().__init__("node_filter")
        self.cut_off = cut_off

    def __str__(self):
        return super().__str__() + " Cut Off: " + str(self.cut_off)


class EdgeFilter(Filter):
    """
    Class for EdgeFilter objects, extends Filter class.

    Instance Attributes:
        edge_transform: type of edge_transform selected, 0: best edges, 1: fuzzy edges, default value is 1.\n
        sc_ratio: Significance Correlation ratio, used in case of fuzzy edges transform\n
        preserve: Preserve cut_off value, used in case of fuzzy edges transform\n
        interpret_abs: Whether to interpret values absolute or not, used in case of fuzzy edges transform
        ignore_self_loops: Saves the preference whether to ignore self loops while applying the edge filter.

    """

    def __init__(self, edge_transform=1, sc_ratio=0.75, preserve=0.2,
                 interpret_abs=False, ignore_self_loops=True):
        """
        Instantiates Edge Filter object.

        :param edge_transform: edge_transform type, default is 1\n
        :param sc_ratio: Significance Correlation ratio, default is 0.75\n
        :param preserve: Preserve cutoff, default is 0.2\n
        :param interpret_abs: Interpret values in absolute manner or not, default is False.\n
        :param ignore_self_loops: Ignore self loops, default is True.\n
        """

        super().__init__("edge_filter")
        self.edge_transform = edge_transform
        self.sc_ratio = sc_ratio
        self.preserve = preserve
        self.interpret_abs = interpret_abs
        self.ignore_self_loops = ignore_self_loops

    def __str__(self):
        if self.edge_transform == 1:
            return super().__str__() + " Edge Transform: " + str(self.edge_transform) + " sc_ratio: " + str(
                self.sc_ratio) + " Preserve: " + str(self.preserve) + " Ignore Self Loops: " + str(
                self.ignore_self_loops) + " Interpret Absolute: " + str(self.interpret_abs)
        else:
            return super().__str__() + "Edge Transform: " + str(self.edge_transform)+" Ignore Self Loops: " + str(self.ignore_self_loops)


class ConcurrencyFilter(Filter):
    """
    Class for ConcurrencyFilter objects, extends Filter class.

    Instance Attributes:
        filter_concurrency: Saves the preference whether to use concurrency filter or not.\n
        preserve: Preserve value\n
        offset: offset value\n
    """

    def __init__(self, filter_concurrency=True, preserve=0.6, offset=0.7):
        super().__init__("concurrency_filter")
        self.filter_concurrency = filter_concurrency
        self.preserve = preserve
        self.offset = offset

    def __str__(self):
        if self.filter_concurrency:
            return super().__str__() + " Preserve: " + str(self.preserve) + " Offset: " + str(self.offset)
        else:
            return super().__str__() + "Filter is Disabled"
