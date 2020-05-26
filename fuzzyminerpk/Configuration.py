import numpy as np


class Configuration:
    def __init__(self, filter_config, metric_configs, attenuation, chunk_size):
        self.filter_config = filter_config
        self.metric_configs = metric_configs
        self.attenuation = attenuation
        self.chunk_size = chunk_size


class FilterConfig:
    def __init__(self, node_filter, edge_filter, concurrency_filter):
        self.node_filter = node_filter
        self.edge_filter = edge_filter
        self.concurrency_filter = concurrency_filter


class MetricConfig:
    """
    name: Metric name
    metric_type: 0 - Unary, 1 - Binary, 2 - Binary Correlation
    include: To include in computation
    invert: Invert the meaning
    weight: Weight of this Metric
    """
    def __init__(self, name, metric_type, include=True, invert=False, weight=0.5):
        self.name = name
        self.metric_type = metric_type
        self.include = include
        self.invert = invert
        self.weight = weight


class AggregateMetric:
    def __init__(self, name):
        self.name = name
