class Configuration:
    """
    Class to hold all the configurations, Filters, Metrics, attenuation and maximal distance value.

    Instance Attributes:
        filter_config: FilterConfig object\n
        metric_config: MetricConfig object\n
        attenuation: Attenuation object\n
        maximal_distance: Maximum distance to consider fuzzy relations\n
    """
    def __init__(self, filter_config, metric_configs, attenuation, maximal_distance):
        self.filter_config = filter_config
        self.metric_configs = metric_configs
        self.attenuation = attenuation
        self.maximal_distance = maximal_distance

    def __str__(self):
        metric_info = ""
        for metric in self.metric_configs:
            metric_info += metric.__str__()
        return self.filter_config.__str__() + "\n" + metric_info + " Attenuation: " + str(
            self.attenuation) + " Maximum Distance: " + str(self.maximal_distance)


class FilterConfig:
    """
    Class for FilterConfig object, holds all three type of filters as attributes.

    Instance Attributes:
        node_filter: node filter object, holds configuration of the node filter\n
        edge_filter: edge filter object, holds configuration of the edge filter\n
        concurrency_filter: concurrency filter object, holds configuration of the concurrency filter\n

    """

    def __init__(self, node_filter, edge_filter, concurrency_filter):
        """
        Instantiates FilterConfig object.
        :param node_filter: node filter object\n
        :param edge_filter: edge filter object\n
        :param concurrency_filter: concurrency filter object\n
        """
        self.node_filter = node_filter
        self.edge_filter = edge_filter
        self.concurrency_filter = concurrency_filter

    def __str__(self):
        return self.node_filter.__str__() + "\n" + self.edge_filter.__str__() + "\n" + self.concurrency_filter.__str__()


class MetricConfig:
    """
    Class for MetricConfig objects

    Instance Attributes:
        name: Name of the metric config\n
        metric_type: saves type of the metric, unary, binary, binary_correlation\n
        include: saves preference to select this metric or not\n
        invert: whether to interpret values in inverted manner\n
        weight: weight of this metric, basically normalize the actual value according to this weight\n
    """

    def __init__(self, name, metric_type, include=True, invert=False, weight=1.0):
        """
        Instantiates the Metric config object.
        :param name: name of metric\n
        :param metric_type: type of metric\n
        :param include: include or not, default value is True\n
        :param invert: invert the interpretation or not, default is False\n
        :param weight: weight value upto which all values should be normalized, default weight is 1.0\n
        """

        self.name = name
        self.metric_type = metric_type
        self.include = include
        self.invert = invert
        self.weight = weight

    def __str__(self):
        return "Metric Name: " + self.name + " Metric Type: " + self.metric_type + " Included: " + str(
            self.include) + " Inverted: " + str(self.invert) + " Weight: " + str(self.weight)
