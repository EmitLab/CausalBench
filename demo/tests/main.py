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

    # ########################################################
    # ######## Abhinav's CB backend integration tests ########
    # ########################################################
    # Metric save test
    # metric0 = Metric()
    # metric0.publish()
    #
    # # # Dataset save test
    # ds0 = Dataset()
    # ds0.publish()

    # # # Model Save test
    # model0 = Model()
    # model0.publish()

    # # Pipeline save test
    # scenario0 = Pipeline()
    # scenario0.publish()

    #     # # Dataset fetch test
    # # ds0 = Dataset(34)
    # # ds0.fetch(34)

    # # # Model fetch test
    # model0 = Model(3) # Model constructor calls fetch()

    # # # Pipeline fetch test
    # scenario0 = Pipeline(3)
    # # scenario0.fetch(1)

    # Metric Fetch test
    # metric0 = Metric(8)
    # metric0.publish()

    # # # Pipeline exec test
    # scenario0 = Pipeline(3)
    # scenario0.execute(access_token)

    # # # static discovery
    # # scenario0 = Pipeline(0)
    # # result0 = scenario0.execute()
    # # display_report(result0)

    # # # temporal discovery
    # # scenario1 = Pipeline(1)
    # # result1 = scenario1.execute()
    # # display_report(result1)

    # # # Classification
    # # scenario2 = Pipeline(2)
    # # result2 = scenario2.execute()
    # # display_report(result2)

    # # manually creation
    # scenario1 = Pipeline.create(name='scenario1',
    #                             task='discovery.temporal',
    #                             dataset=2,
    #                             model=(Model(0), {'data': 'file1'}),
    #                             metrics=[(0, {'ground_truth': 'file2'}),
    #                                      (1, {'ground_truth': 'file2'}),
    #                                      (2, {'ground_truth': 'file2'}),
    #                                      (3, {'ground_truth': 'file2'}),
    #                                      (4, {'ground_truth': 'file2'})])
    # # result1 = scenario1.execute()
    # # display_report(result1)
    # scenario1.publish()

    dataset1 = Dataset(zip_file='data/abalone.zip')
    # dataset1.publish()

    model1 = Model(zip_file='model/ges.zip')
    # model1.publish()

    metric1 = Metric(zip_file='metric/accuracy_static.zip')
    # metric1.publish()

    # scenario1 = Pipeline.create(name='scenario1',
    #                             description='Pipeline to evaluate GES algorithm on Abalone dataset',
    #                             task='discovery.static',
    #                             dataset=dataset1,
    #                             model=(model1, {'data': 'file1'}),
    #                             metrics=[(metric1, {'ground_truth': 'file2'})])
    # scenario1.publish()
    #
    # run1: Run = scenario1.execute()
    # run1.publish()
    # print(run1)

    # scenario1 = Scenario.create(name='scenario5',
    #                             description='Scenario to evaluate GES algorithm on Abalone dataset',
    #                             task='discovery.static',
    #                             dataset=dataset1,
    #                             model=(model1, {'data': 'file1'}),
    #                             metrics=[(metric1, {'ground_truth': 'file2'}),
    #                                      (metric1, {'ground_truth': 'file2'})])
    # # # scenario1 = Pipeline(31)
    # # # # scenario1.publish()
    # # #
    # run1 = scenario1.execute()
    # print(run1)
    # # # run1.publish()

    # task: Task = Task(module_id='discovery.static')
    # obj: AbstractTask = task.load()
    # helpers = obj.helpers()
    # print(helpers.hello())

    context: Context = Context.create(name='Context1',
                                      description='Test context',
                                      task='discovery.static',
                                      datasets=[(dataset1, {'data': 'file1', 'ground_truth': 'file2'})],
                                      models=[(model1, {})],
                                      metrics=[(metric1, {})])

    context.execute()


if __name__ == '__main__':
    main()
