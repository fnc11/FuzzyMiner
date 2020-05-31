import numpy as np


class Filter:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Filter name: " + self.name


class NodeFilter(Filter):
    def __init__(self, cut_off=0.0):
        super().__init__("node_filter")
        self.cut_off = cut_off

    def __str__(self):
        return super().__str__() + " Cut Off: " + str(self.cut_off)


# Edge transform 0: best edges, 1: fuzzy edges
class EdgeFilter(Filter):
    def __init__(self, edge_transform=1, sc_ratio=0.75, cut_off=0.2,
                 ignore_self_loops=True, interpret_abs=False):
        super().__init__("edge_filter")
        self.edge_transform = edge_transform
        self.sc_ratio = sc_ratio
        self.cut_off = cut_off
        self.ignore_self_loops = ignore_self_loops
        self.interpret_abs = interpret_abs

    def __str__(self):
        if self.edge_transform == 1:
            return super().__str__() + " Edge Transform: " + str(self.edge_transform) + " sc_ratio: " + str(
                self.sc_ratio) + " Cut Off: " + str(self.cut_off) + " Ignore Self Loops: " + str(
                self.ignore_self_loops) + " Interpret Absolute: " + str(self.interpret_abs)
        else:
            return super().__str__() + "Edge Transform: " + str(self.edge_transform)


class ConcurrencyFilter(Filter):
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
