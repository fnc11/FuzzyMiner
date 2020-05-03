
class Configuration:
    pass


class FilterConfig:
    pass


class MetricConfig:
    def __init__(self, name, metric_type, include, invert, weight):
        self.name = name
        self.metric_type = metric_type
        self.include = include
        self.invert = invert
        self.weight = weight


