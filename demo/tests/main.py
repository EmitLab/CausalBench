import networkx as nx
import json
import requests

from demo.causalbench.modules.dataset import Dataset
from demo.causalbench.modules.model import Model
from demo.causalbench.modules.pipeline import Pipeline
from demo.causalbench.modules.metric import Metric
from demo.causalbench import access_token
import numpy as np
from matplotlib import pyplot as plt

# from causalbench.commons.utils import display_report
# from causalbench.modules.pipeline import Pipeline

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
    import sys
    sys.path.insert(0,'model/ermirmcfcminst')

    # ########################################################
    # ######## Abhinav's CB backend integration tests ########
    # ########################################################
    # Metric save test
    # metric0 = Metric()
    # metric0.publish()

    # # Dataset save test
    ds0 = Dataset()
    ds0.publish()

    # # # Model Save test
    # model0 = Model()
    # model0.publish()

    # # Pipeline save test
    # pipeline0 = Pipeline()
    # pipeline0.publish()

    #     # # Dataset fetch test
    # # ds0 = Dataset(34)
    # # ds0.fetch(34)

    # # # Model fetch test
    # model0 = Model(3) # Model constructor calls fetch()

    # # # Pipeline fetch test
    # pipeline0 = Pipeline(3)
    # # pipeline0.fetch(1)

    # Metric Fetch test
    # metric0 = Metric(8)
    # metric0.publish()

    # # # Pipeline exec test
    # pipeline0 = Pipeline(3)
    # pipeline0.execute()

        # # # static discovery
        # # pipeline0 = Pipeline(0)
        # # result0 = pipeline0.execute()
        # # display_report(result0)

        # # # temporal discovery
        # # pipeline1 = Pipeline(1)
        # # result1 = pipeline1.execute()
        # # display_report(result1)
        
        # # # Classification
        # # pipeline2 = Pipeline(2)
        # # result2 = pipeline2.execute()
        # # display_report(result2)

        # # manually creation
        # # pipeline1 = Pipeline()
        # # pipeline1.create(name='pipeline1',
        # #                  task='discovery.temporal',
        # #                  dataset=2,
        # #                  model=(Model(0), {'data': 'file1'}),
        # #                  metrics=[(0, {'ground_truth': 'file2'}),
        # #                           (1, {'ground_truth': 'file2'}),
        # #                           (2, {'ground_truth': 'file2'}),
        # #                           (3, {'ground_truth': 'file2'}),
        # #                           (4, {'ground_truth': 'file2'})])
        # # result1 = pipeline1.execute()
        # # display_report(result1)
        # # pipeline1.publish()

if __name__ == '__main__':
    main()
