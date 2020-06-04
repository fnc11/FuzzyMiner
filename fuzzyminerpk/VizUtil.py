import math
import random
import string

from graphviz import Digraph

GRAPH_PATH = 'media/graphs/'
GRAPH_FORMAT = 'png'
NODE_COLORS = ['#c4ecf2', '#a9e8f2', '#6bd9ec', '#54d6ea', '#0cb6d1', '#0cb6d1']
CLUSTER_COLORS = ['', '', '', '', '', '']

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

        filename = ''.join(random.choice(string.ascii_lowercase) for i in range(16)) + '.gv'
        dot = Digraph(name='Fuzzy Model',
                      filename=filename,
                      directory=GRAPH_PATH, format=GRAPH_FORMAT)
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
            dot.node(str(node.index), label=label, penwidth='1.0', fillcolor=NODE_COLORS[int(node.significance*5)])

        for cluster in self.fm_clusters:
            label = ''.join([cluster.label, ' ', str(cluster.index), ' ~ ', str(len(cluster.primitives)), ' primitives'])
            label = ''.join([label, '\n mean_sig: ', self.format(cluster.significance)])
            dot.node(str(cluster.index), label=label, shape='oval', color='#a7df40')

        dot.edge_attr['fontsize'] = '10.0'
        for edge in self.fm_edges:
            label = " sig: " + self.format(edge.significance) + "\n" + " cor: " + self.format(edge.correlation)
            pen_width = self.pen_width(edge.significance)
            dot.edge(str(edge.source), str(edge.target), label=label, constraint='true', penwidth=pen_width, color ='#FF5F49')
        # print(dot.source)
        # dot.render(view=True)
        dot.render()
        graph_path = ''.join(['/', GRAPH_PATH, filename, '.', GRAPH_FORMAT])
        # print(graph_path)
        return graph_path

    def pen_width(self, significance):
        return str(math.ceil((significance * 10) / 2))

    def format(self, significance):
        return "{:.3f}".format(significance)
