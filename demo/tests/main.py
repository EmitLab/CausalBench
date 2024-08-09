import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from causalbench.modules import Dataset, Metric, Model, Scenario, Run
from causalbench.modules.context import Context
from causalbench.modules.task import Task, AbstractTask


# from causalbench.commons.utils import display_report
# from causalbench.modules.scenario import Pipeline

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
    # import sys
    # sys.path.insert(0, 'model/ermirmcfcminst')
    # access_token = init_auth()

    dataset1 = Dataset(zip_file='data/abalone.zip')
    # dataset1.publish(public=True)

    dataset2 = Dataset(zip_file='data/time_series_simulated.zip')

    model1 = Model(zip_file='model/pc.zip')
    # model1.publish()

    model2 = Model(zip_file='model/ges.zip')
    # model2.publish()

    model3 = Model(zip_file='model/varlingam.zip')

    metric1 = Metric(zip_file='metric/precision_static.zip')
    # metric1.publish()

    metric2 = Metric(zip_file='metric/recall_static.zip')
    # metric2.publish()

    metric3 = Metric(zip_file='metric/accuracy_temporal.zip')
    metric4 = Metric(zip_file='metric/shd_temporal.zip')

    # static task
    context1: Context = Context.create(name='Context1',
                                      description='Test static task',
                                      task='discovery.static',
                                      datasets=[(dataset1, {'data': 'file1', 'ground_truth': 'file2'})],
                                      models=[(model1, {}),
                                              (model2, {})],
                                      metrics=[(metric1, {}),
                                               (metric2, {})])

    context1.execute()

    # temporal task
    context2: Context = Context.create(name='Context2',
                                      description='Test temporal task',
                                      task='discovery.temporal',
                                      datasets=[(dataset2, {'data': 'file1', 'ground_truth': 'file2'})],
                                      models=[(model3, {})],
                                      metrics=[(metric3, {}),
                                               (metric4, {})])
    context2.execute()

if __name__ == '__main__':
    main()
