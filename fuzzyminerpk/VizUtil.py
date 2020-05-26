import math

from graphviz import Digraph


class VizUtil:

    def __init__(self):
        self.fm_nodes = None
        self.fm_edges = None
        self.fm_clusters = None

    def visualize(self, fm_nodes, fm_edges, fm_clusters, drop_disconnected_nodes=True):
        self.fm_nodes = fm_nodes
        self.fm_edges = fm_edges
        self.fm_clusters = fm_clusters

        connected_node_indices = set()
        if drop_disconnected_nodes:
            for edge in self.fm_edges:
                connected_node_indices.add(edge.source)
                connected_node_indices.add(edge.target)

        dot = Digraph(name='Fuzzy Model', filename='fuzzy.gv', directory='media/graphs/', format='png')
        dot.node_attr['shape'] = 'rectangle'
        dot.node_attr['style'] = 'filled'
        dot.node_attr['fontcolor'] = 'black'
        dot.node_attr['fontsize'] = '12.0'
        dot.node_attr['pencolor'] = 'black'

        for node in self.fm_nodes:
            if drop_disconnected_nodes and node.index not in connected_node_indices:
                continue
            tokens = node.label.split('@')
            if len(tokens) == 0:
                continue
            if len(tokens) > 1:
                label = tokens[0] + "\n" + tokens[1]
            else:
                label = tokens[0]
            label += "\n" + self.format(node.significance)
            dot.node(str(node.index), label=label, penwidth='1.0', fillcolor='blanchedalmond')

        for cluster in self.fm_clusters:
            dot.node(str(cluster.index), label=cluster.label, shape='oval', color='cadetblue1')
        # dot.node('L', label='Sir Lancelot the Brave', style='filled', color='blue', fontcolor='white')

        # dot.edges(['AB', 'AL'])
        dot.edge_attr['fontsize'] = '10.0'
        for edge in self.fm_edges:
            label = " sig: " + self.format(edge.significance) + "\n" + " cor: " + self.format(edge.correlation)
            pen_width = self.thickness(edge.significance)
            dot.edge(str(edge.source), str(edge.target), label=label, constraint='true', penwidth=pen_width)
        # dot.edge('B', 'L', constraint='false', arrowsize='4.0')
        print(dot.source)
        dot.render(view=True)

    def thickness(self, significance):
        return str(math.ceil((significance * 10) / 2))

    def format(self, significance):
        return "{:.3f}".format(significance)
