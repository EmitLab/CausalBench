import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from causalbench.commons.utils import display_report
from causalbench.modules.pipeline import Pipeline


def plot_graph(matrix, nodes, pos=None, title=None, figsize=(10, 6), dpi=None):
    plt.figure(figsize=figsize, dpi=dpi)

    rows, cols = np.where(matrix == 1)
    edges = zip(rows.tolist(), cols.tolist())
    labels = {i: label for i, label in enumerate(nodes)}

    graph = nx.DiGraph()
    graph.add_nodes_from(range(len(nodes)))
    graph.add_edges_from(edges)

    if pos is None:
        pos = nx.arf_layout(graph)

    nx.draw_networkx_nodes(graph, pos,
                           node_size=[len(labels[i]) * 500 for i in graph.nodes],
                           node_color='#5F9EA0')
    nx.draw_networkx_edges(graph, pos,
                           node_size=[len(labels[i]) * 500 for i in graph.nodes],
                           edge_color='#666666',
                           arrowsize=15,
                           connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_labels(graph, pos, labels,
                            font_color='white')

    plt.title(label=title, pad=30, fontsize=20, color='#CD5C5C')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return graph, pos


def main():
    pipeline0 = Pipeline(0)
    result0 = pipeline0.execute()
    display_report(result0)

    # pipeline1 = Pipeline()
    # pipeline1.create(name='pipeline1',
    #                  task='discovery.temporal',
    #                  dataset=2,
    #                  model=(Model(0), {'data': 'file1'}),
    #                  metrics=[(0, {'ground_truth': 'file2'}),
    #                           (1, {'ground_truth': 'file2'}),
    #                           (2, {'ground_truth': 'file2'}),
    #                           (3, {'ground_truth': 'file2'}),
    #                           (4, {'ground_truth': 'file2'})])
    # result1 = pipeline1.execute()
    # display_report(result1)
    # pipeline1.publish()


if __name__ == '__main__':
    main()
