import numpy as np


class Filter:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Filter name: " + self.name


class NodeFilter(Filter):
    def __init__(self, name="node_filter", cut_off=0.5):
        super().__init__(name)
        self.cut_off = cut_off

    def __str__(self):
        return super().__str__() + " Cut Off: " + str(self.cut_off)


class EdgeFilter(Filter):
    def __init__(self, name="edge_filter", edge_transform="Fuzzy", sc_ratio=0.5, cut_off=0.5,
                 ignore_self_loops=False, interpret_abs=False):
        super().__init__(name)
        self.edge_transform = edge_transform
        self.sc_ratio = sc_ratio
        self.cut_off = cut_off
        self.ignore_self_loops = ignore_self_loops
        self.interpret_abs = interpret_abs

    def __str__(self):
        if self.edge_transform == "Fuzzy Edges":
            return super().__str__() + " Edge Transform: " + self.edge_transform + " sc_ratio: " + str(
                self.sc_ratio) + " Cut Off: " + str(self.cut_off) + " Ignore Self Loops: " + str(
                self.ignore_self_loops) + " Interpret Absolute: " + str(self.interpret_abs)
        else:
            return super().__str__() + "Edge Transform: " + self.edge_transform


class ConcurrencyFilter(Filter):
    def __init__(self, name="concurrency_filter", filter_concurrency=True, preserve=0.5, offset=0.5):
        super().__init__(name)
        self.filter_concurrency = filter_concurrency
        self.preserve = preserve
        self.offset = offset

    def __str__(self):
        if self.filter_concurrency:
            return super().__str__() + " Preserve: " + str(self.preserve) + " Offset: " + str(self.offset)
        else:
            return super().__str__() + "Filter is Disabled"
