import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from causalbench.modules import Dataset, Metric, Model, Context, Run
from causalbench.modules.task import Task, AbstractTask
from causalbench.commons.utils import package_module

from importlib.metadata import version


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
    # dataset1 = Dataset(module_id=1, version=1)
    # dataset1 = Dataset(zip_file='data/abalone.zip')
    # dataset1.publish()

    # dataset2 = Dataset(module_id=2, version=1)
    # dataset2 = Dataset(zip_file='data/time_series_simulated.zip')
    # dataset2.publish()

    # dataset3 = Dataset(zip_file='data/sachs.zip')
    # dataset3.publish()

    # model1 = Model(module_id=1, version=1)
    # model1 = Model(zip_file='model/pc.zip')
    # model1.publish()

    # model2 = Model(module_id=2, version=1)
    # model2 = Model(zip_file='model/ges.zip')
    # model2.publish()

    # model3 = Model(module_id=3, version=1)
    # model3 = Model(zip_file='model/varlingam.zip')
    # model3.publish()

    # model4 = Model(module_id=4, version=1)
    # model4 = Model(zip_file='model/pcmciplus.zip')
    # model4.publish()

    # metric1 = Metric(module_id=1, version=1)
    # metric1 = Metric(zip_file='metric/accuracy_static.zip')
    # metric1.publish()

    # metric2 = Metric(module_id=2, version=1)
    # metric2 = Metric(zip_file='metric/f1_static.zip')
    # metric2.publish()

    # metric3 = Metric(module_id=3, version=1)
    # metric3 = Metric(zip_file='metric/accuracy_temporal.zip')
    # metric3.publish()

    # metric4 = Metric(module_id=4, version=1)
    # metric4 = Metric(zip_file='metric/shd_temporal.zip')
    # metric4.publish()

    # task: Task = Task(module_id='discovery.temporal')
    # task.load()

    # static task
    # context1: Context = Context(module_id=10, version=6)
    # context1: Context = Context.create(name='Context2',
    #                                    description='Test static context',
    #                                    task='discovery.static',
    #                                    datasets=[(dataset1, {'data': 'file1', 'ground_truth': 'file2'})],
    #                                    models=[(model1, {'alpha': 0.001}),
    #                                            (model2, {})],
    #                                    metrics=[(metric1, {}),
    #                                             (metric2, {})])

    # context1: Context = Context.create(module_id=10,
    #                                    name='Context1',
    #                                    description='Test static context',
    #                                    task='discovery.static',
    #                                    datasets=[(dataset1, {'data': 'file1', 'ground_truth': 'file2'})],
    #                                    models=[(model1, {'alpha': 0.001, 'variant': 'stable'}),],
    #                                    metrics=[(metric1, {'binarize': False})])
    # context1.publish()
    # context1.publish(public=True)

    # run: Run = context1.execute()
    # # run.publish(public=True)
    # print(run)
    #
    # # temporal task
    # # context2: Context = Context(module_id=3, version=1)
    # context2: Context = Context.create(module_id=11,
    #                                    name='Temporal Context: VAR-LiNGAM, pcmciplus',
    #                                    description='Test temporal context',
    #                                    task='discovery.temporal',
    #                                    datasets=[(dataset2, {'data': 'file1', 'ground_truth': 'file2'})],
    #                                    models=[(model3, {}), (model4, {'tau_min': 1})],
    #                                    metrics=[(metric3, {}), (metric4, {})])
    # # context2.publish(public=True)
    #
    # run: Run = context2.execute()
    # # run.publish(public=True)
    # print(run)

    # print(version('causalbench-asu'))

    # context: Context = Context(module_id=2, version=1)
    # run: Run = context.execute()
    # print(run)
    # run.publish()

    # run: Run = context.execute()
    # print(run)
    # run.publish()

    # dataset: Dataset = Dataset(zip_file='data/time_series_simulated.zip', module_id=1444)
    # dataset.publish()

    # model: Model = Model(zip_file='model/ges.zip', module_id=2)
    # model.publish()

    # metric: Metric = Metric(zip_file='metric/accuracy_temporal.zip', module_id=2)
    # metric.publish(public=True)


    # TEMPORAL
    # dataset1: Dataset = Dataset(module_id=1444, version=2)
    # dataset2: Dataset = Dataset(module_id=1447, version=2)
    #
    # model1: Model = Model(module_id=4, version=1)  # PCMCI+
    # # model2: Model = Model(module_id=5, version=1)  # VAR-LiNGAM
    #
    # metric1: Metric = Metric(module_id=2, version=2)
    # metric2: Metric = Metric(module_id=4, version=4)
    # metric3: Metric = Metric(module_id=6, version=3)
    # metric4: Metric = Metric(module_id=8, version=3)
    # metric5: Metric = Metric(module_id=10, version=2)
    #
    # pcmciplus_models_list = []
    # alphas = np.linspace(0.001, 0.1, 20).tolist()
    # max_conds_dims = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # for alpha in alphas:
    #     for max_conds_dim in max_conds_dims:
    #         pcmciplus_models_list.append((model1, {'tau_min': 1, 'max_conds_dim': max_conds_dim, 'alpha': alpha}))
    #
    # context1: Context = Context.create(module_id=10,
    #                                    task='discovery.temporal',
    #                                    name='Benchmark (hyperparameters): PCMCIplus',
    #                                    description='Benchmark hyperparameters for PCMCIplus algorithm',
    #                                    datasets=[
    #                                        (dataset1, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                        (dataset2, {'data': 'file1', 'ground_truth': 'file2'})
    #                                    ],
    #                                    models=pcmciplus_models_list,
    #                                    metrics=[(metric1, {}), (metric2, {}), (metric3, {}), (metric4, {}), (metric5, {})])
    #
    # context1.publish()



    # varlingam_models_list = []
    # criterias = ['aic', 'fpe', 'hqic', 'bic']
    # prunes = [True, False]
    # for criteria in criterias:
    #     for prune in prunes:
    #         varlingam_models_list.append((model2, {'criterion': criteria, 'prune': prune}))
    #
    # context2: Context = Context.create(task='discovery.temporal',
    #                                    name='Benchmark (hyperparameters): VAR-LiNGAM',
    #                                    description='Benchmark hyperparameters for VAR-LiNGAM algorithm',
    #                                    datasets=[
    #                                        (dataset1, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                        (dataset2, {'data': 'file1', 'ground_truth': 'file2'})
    #                                    ],
    #                                    models=varlingam_models_list,
    #                                    metrics=[(metric1, {}), (metric2, {}), (metric3, {}), (metric4, {}), (metric5, {})])
    #
    # context2.publish()





    # STATIC
    # dataset1 = Dataset(module_id=1, version=1)
    # dataset2 = Dataset(module_id=1443, version=1)
    # dataset3 = Dataset(module_id=350, version=1)
    # dataset4 = Dataset(module_id=1185, version=1)
    # dataset5 = Dataset(module_id=1437, version=1)
    #
    # model3 = Model(module_id=3, version=1)  # PC
    #
    # metric1 = Metric(module_id=1, version=1)
    # metric2 = Metric(module_id=3, version=1)
    # metric3 = Metric(module_id=5, version=1)
    # metric4 = Metric(module_id=7, version=1)
    #
    # pc_models_list = []
    # alphas = np.linspace(0.001, 0.1, 20).tolist()
    # variants = ['original', 'stable']
    # for alpha in alphas:
    #     for variant in variants:
    #         pc_models_list.append((model3, {'variant': variant, 'alpha': alpha}))
    #
    # context3: Context = Context.create(module_id=12,
    #                                    task='discovery.static',
    #                                    name='Benchmark (hyperparameters): PC',
    #                                    description='Benchmark hyperparameters for PC algorithm',
    #                                    datasets=[(dataset1, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                              (dataset2, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                              (dataset3, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                              (dataset4, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                              (dataset5, {'data': 'file1', 'ground_truth': 'file2'})
    #                                              ],
    #                                    models=pc_models_list,
    #                                    metrics=[(metric1, {}), (metric2, {}), (metric3, {}), (metric4, {})])
    #
    # context3.publish()


    # dataset1: Dataset = Dataset(module_id=1444, version=2)
    # dataset2: Dataset = Dataset(module_id=1447, version=2)
    #
    # model1: Model = Model(module_id=4, version=1)  # PCMCI+
    # model2: Model = Model(module_id=5, version=1)  # VAR-LiNGAM
    #
    # metric1: Metric = Metric(module_id=2, version=2)
    # metric2: Metric = Metric(module_id=4, version=4)
    # metric3: Metric = Metric(module_id=6, version=3)
    # metric4: Metric = Metric(module_id=8, version=3)
    # metric5: Metric = Metric(module_id=10, version=2)
    #
    # models_list = []
    #
    # alphas = [0.001, 0.005, 0.01, 0.025, 0.05]
    # max_conds_dims = [1, 2, 3, 4, 5]
    # for alpha in alphas:
    #     for max_conds_dim in max_conds_dims:
    #         models_list.append((model1, {'tau_min': 1, 'max_conds_dim': max_conds_dim, 'alpha': alpha}))
    #
    # criterias = ['aic', 'fpe', 'hqic', 'bic']
    # prunes = [True, False]
    # for criteria in criterias:
    #     for prune in prunes:
    #         models_list.append((model2, {'criterion': criteria, 'prune': prune}))
    #
    # context1: Context = Context.create(task='discovery.temporal',
    #                                    name='Benchmark (hyperparameters): VAR-LiNGAM, PCMCIplus',
    #                                    description='Benchmark hyperparameters for temporal causal discovery algorithms across multiple datasets',
    #                                    datasets=[
    #                                        (dataset1, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                        (dataset2, {'data': 'file1', 'ground_truth': 'file2'})
    #                                    ],
    #                                    models=models_list,
    #                                    metrics=[(metric1, {}), (metric2, {}), (metric3, {}), (metric4, {}), (metric5, {})])
    #
    # context1.publish()

    # dataset1 = Dataset(module_id=1, version=1)
    # dataset2 = Dataset(module_id=1443, version=1)
    # dataset3 = Dataset(module_id=350, version=1)
    # dataset4 = Dataset(module_id=1185, version=1)
    # dataset5 = Dataset(module_id=1437, version=1)
    #
    # # model1 = Model(module_id=2, version=1)  # ges
    # model2 = Model(module_id=3, version=1)  # pc
    # # model3 = Model(module_id=4, version=1) #pcmci
    # # model4 = Model(module_id=5, version=1) #varlingam
    #
    # metric1 = Metric(module_id=1, version=1)
    # metric2 = Metric(module_id=3, version=1)
    # metric3 = Metric(module_id=5, version=1)
    # metric4 = Metric(module_id=7, version=1)
    # # metric5 = Metric(module_id=9, version=1)
    # # # #
    #
    #
    # # methods = ['scatter', 'r2']
    # models_list = []
    # # for method in methods:
    # #     models_list.append((model1, {'method': method}))
    #
    # alphas = [0.01, 0.02, 0.03, 0.04, 0.05]
    # variants = ['original', 'stable']
    # for variant in variants:
    #     for alpha in alphas:
    #         models_list.append((model2, {'variant': variant, 'alpha': alpha}))
    #
    # context1: Context = Context.create(task='discovery.static',
    #                                    name='Benchmark (hyperparameters): PC',  # 'CB-StaticDiscovery',
    #                                    description='Benchmark hyperparameters for static causal discovery algorithm PC across multiple datasets',
    #                                    datasets=[(dataset1, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                              (dataset2, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                              (dataset3, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                              (dataset4, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                              (dataset5, {'data': 'file1', 'ground_truth': 'file2'})
    #                                              ],
    #                                    models=models_list,
    #                                    metrics=[(metric1, {}),  # 'threshold': 0.03
    #                                             (metric2, {}),
    #                                             (metric3, {}),
    #                                             (metric4, {})])
    #
    # context1.publish()



    # dataset1: Dataset = Dataset(module_id=1444, version=2)
    # dataset2: Dataset = Dataset(module_id=1447, version=2)
    #
    # model1: Model = Model(module_id=4, version=1)
    # model2: Model = Model(module_id=5, version=1)
    #
    # metric1: Metric = Metric(module_id=2, version=2)
    # metric2: Metric = Metric(module_id=4, version=4)
    # metric3: Metric = Metric(module_id=6, version=3)
    # metric4: Metric = Metric(module_id=8, version=3)
    # metric5: Metric = Metric(module_id=10, version=2)
    #
    # context1: Context = Context.create(module_id=6,
    #                                    task='discovery.temporal',
    #                                    name='Benchmark: VAR-LiNGAM, PCMCIplus',
    #                                    description='Benchmark temporal causal discovery algorithms across multiple datasets',
    #                                    datasets=[
    #                                        (dataset1, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                        (dataset2, {'data': 'file1', 'ground_truth': 'file2'})
    #                                    ],
    #                                    models=[(model1, {'tau_min': 1}), (model2, {})],
    #                                    metrics=[(metric1, {}), (metric2, {}), (metric3, {}), (metric4, {}), (metric5, {})])
    #
    # context1.publish()
    #
    # context1: Context = Context(module_id=6, version=3)
    # run: Run = context1.execute()
    # print(run)
    # # run.publish(public=True)
    #
    # state = run.__getstate__()
    # zip_file = package_module(state, None)
    # shutil.copy(zip_file, os.getcwd())

    dataset1: Dataset = Dataset(module_id=1444, version=2)
    # dataset2: Dataset = Dataset(module_id=1446, version=2)
    #
    # model1: Model = Model(module_id=4, version=1)  # PCMCI+
    #
    # metric1: Metric = Metric(module_id=2, version=2)
    # metric2: Metric = Metric(module_id=4, version=4)
    # metric3: Metric = Metric(module_id=6, version=3)
    # metric4: Metric = Metric(module_id=8, version=3)
    # metric5: Metric = Metric(module_id=10, version=2)
    #
    # context1: Context = Context.create(task='discovery.temporal',
    #                                    name='Benchmark: PCMCIplus on Telecom and time_sim datasets',
    #                                    description='Benchmark hyperparameters for PCMCIplus algorithm',
    #                                    datasets=[
    #                                        (dataset1, {'data': 'file1', 'ground_truth': 'file2'}),
    #                                        (dataset2, {'data': 'file1', 'ground_truth': 'file2'})
    #                                    ],
    #                                    models=[(model1, {})],
    #                                    metrics=[(metric1, {}), (metric2, {}), (metric3, {}), (metric4, {}), (metric5, {})])
    #
    # context1.publish(public=True)


if __name__ == '__main__':
    main()
