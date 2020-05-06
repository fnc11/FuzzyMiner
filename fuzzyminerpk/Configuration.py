
class Configuration:
    def __init__(self, filter_config, metric_configs):
        self.filter_config = filter_config
        self.metric_configs = metric_configs


class FilterConfig:
    def __init__(self, node_filter, edge_filter, concurrency_filter):
        self.node_filter = node_filter
        self.edge_filter = edge_filter
        self.concurrency_filter = concurrency_filter


class MetricConfig:
    def __init__(self, name, metric_type, include=True, invert=False):
        self.name = name
        self.metric_type = metric_type
        self.include = include
        self.invert = invert


class MetricWeight:
    def __init__(self, name, include=True, invert=False):
        self.name = name
        self.include = include
        self.invert = invert
