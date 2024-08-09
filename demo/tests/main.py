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

    # dataset1 = Dataset(module_id=9, version=3)
    # dataset1 = Dataset(zip_file='data/abalone.zip')
    # dataset1.publish(public=True)

    # model1 = Model(module_id=4, version=1)
    # model1 = Model(zip_file='model/pc.zip')
    # model1.publish(public=True)

    # model2 = Model(module_id=5, version=1)
    # model2 = Model(zip_file='model/ges.zip')
    # model2.publish(public=True)

    # metric1 = Metric(module_id=8, version=1)
    # metric1 = Metric(zip_file='metric/accuracy_static.zip')
    # metric1.publish(public=True)

    # metric2 = Metric(module_id=9, version=1)
    # metric2 = Metric(zip_file='metric/f1_static.zip')
    # metric2.publish(public=True)

    # context: Context = Context(module_id=10, version=6)
    # context: Context = Context.create(module_id=10,
    #                                   name='Context1',
    #                                   description='Test context',
    #                                   task='discovery.static',
    #                                   datasets=[(dataset1, {'data': 'file1', 'ground_truth': 'file2'})],
    #                                   models=[model1, model2],
    #                                   metrics=[metric1, metric2])
    # context.publish(public=True)

    # run: Run = context.execute()
    # run.publish(public=True)
    # print(run)

    run: Run = Run(module_id=2)
    print(run)


if __name__ == '__main__':
    main()
