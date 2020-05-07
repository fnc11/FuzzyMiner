class Filter:
    def __init__(self, name):
        self.name = name


class NodeFilter(Filter):
    def __init__(self, name="node_filter", cut_off=0.5):
        super().__init__(name)
        self.cut_off = cut_off


class EdgeFilter(Filter):
    def __init__(self, name="edge_filter", edge_transform=True, sc_ratio=0.5, cut_off=0.5,
                 ignore_self_loops=False, interpret_abs=False):
        super().__init__(name)
        self.edge_transform = edge_transform
        self.sc_ratio = sc_ratio
        self.cut_off = cut_off
        self.ignore_self_loops = ignore_self_loops
        self.interpret_abs = interpret_abs


class ConcurrencyFilter(Filter):
    def __init__(self, name="concurrency_filter", filter_concurrency=True, preserve=0.5, offset=0.5):
        super().__init__(name)
        self.filter_concurrency = filter_concurrency
        self.preserve = preserve
        self.offset = offset
