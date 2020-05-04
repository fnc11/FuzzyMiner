
class Filter:
    def __init__(self, name):
        self.name = name


class NodeFilter(Filter):
    def __init__(self, name, cut_off):
        super.__init__(name)
        super().__init__(name)
        self.cut_off = cut_off


class EdgeFilter(Filter):
    def __init__(self, name, edge_transform, sc_ratio, cut_off, ignore_self_loops, interpret_abs):
        super.__init__(name)
        super().__init__(name)
        self.edge_transform = edge_transform
        self.sc_ratio = sc_ratio
        self.cut_off = cut_off
        self.ignore_self_loops = ignore_self_loops
        self.interpret_abs = interpret_abs


class ConcurrencyFilter(Filter):
    def __init__(self, name, filter_concurrency, preserve, balance):
        super.__init__(name)
        super().__init__(name)
        self.filter_concurrency = filter_concurrency
        self.preserve = preserve
        self.balance = balance
