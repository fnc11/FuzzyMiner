
class Configuration:
    def __init__(self, filter_config, metric_configs):
        self.filter_config = filter_config
        self.metric_configs = metric_configs

    def weighted_configuration(self, fuzzy_config):
        # aggregating configuration weights for metrics
        node_sig_weights_freq = 0.5
        node_sig_weights_routing = 0.5
        sig_weights_freq = 0.5
        sig_weights_dist = 0.5
        corr_weights_prox = 0.5
        corr_weights_endpoint = 0.5
        corr_weights_originator = 0.5
        corr_weights_datatype = 0.5
        corr_weights_datavalue = 0.5
        edge_sig_to_corr_ratio = 0.75

        # calculating aggregate node significance values
        agg_node_sig = (fuzzy_config.metric_configs[0] * node_sig_weights_freq) + (
                    fuzzy_config.metric_configs[1] * node_sig_weights_routing)
        max_agg_node_sig_value = max(agg_node_sig)
        # normalized_values
        agg_node_sig = agg_node_sig / max_agg_node_sig_value

        # calculating aggregate edge significance values
        agg_edge_sig = (fuzzy_config.metric_configs[2] * sig_weights_freq) + (
                    fuzzy_config.metric_configs[3] * sig_weights_dist)
        max_agg_edge_sig_value = max(agg_edge_sig)
        # normalized values
        agg_edge_sig = agg_edge_sig / max_agg_edge_sig_value

        # calculating aggregate edge correlation values
        agg_edge_corr = (fuzzy_config.metric_configs[4] * corr_weights_prox) + \
                        (fuzzy_config.metric_configs[5] * corr_weights_endpoint) + \
                        (fuzzy_config.metric_configs[6] * corr_weights_datatype) + \
                        (fuzzy_config.metric_configs[7] * corr_weights_datavalue) + \
                        (fuzzy_config.metric_configs[8] * corr_weights_originator)
        max_agg_edge_corr_value = max(agg_edge_corr)
        # normalized values
        agg_edge_corr = agg_edge_corr / max_agg_edge_corr_value

        # Taking weighted average of agg_edge_sig and agg_edge_corr
        agg_edge_values = (agg_edge_sig * edge_sig_to_corr_ratio) + agg_edge_corr * (1 - edge_sig_to_corr_ratio)
        max_agg_edge_value = max(agg_edge_values)
        # normalize values
        agg_edge_values = agg_edge_values / max_agg_edge_value
        aggregate_weights = [agg_node_sig, agg_edge_sig, agg_edge_corr, agg_edge_values]

        fuzzy_config_weighted = MetricWeight(aggregate_weights, True, False)
        return fuzzy_config_weighted


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
    def __init__(self, name, aggregate_weights, include=True, invert=False):
        self.name = name
        self.aggregate_weights = aggregate_weights
        self.include = include
        self.invert = invert
