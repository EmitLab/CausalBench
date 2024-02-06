import networkx as nx
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from commons import executor
from modules.dataset import Dataset
from modules.metric import Metric
from modules.model import Model


def execute_and_report(module_path, function_name, /, *args, **keywords):
    try:
        response = executor.execute(module_path, function_name, *args, **keywords)

        print('-' * 80)
        print(f'Module: {module_path}')
        print()

        print('Output:')
        print(response["output"])
        print()

        print(f'Duration: {response["duration"]} nanoseconds')
        print(f'Used Memory: {response["memory"]} bytes')
        if response["gpu_memory"] is None:
            print(f'Used GPU Memory: None')
        else:
            print(f'Used GPU Memory: {response["gpu_memory"]} bytes')
        print()

        print(f'Python: {response["python"]}')
        print(f'Imports: {response["imports"]}')
        print()

        print(f'Platform: {response["platform"]}')
        print(f'Processor: {response["processor"]}')
        print(f'GPU: {response["gpu"]}')
        print(f'Architecture: {response["architecture"]}')
        print(f'Total Memory: {response["memory_total"]} bytes')
        if response["gpu_memory_total"] is None:
            print(f'Total GPU Memory: None')
        else:
            print(f'Total GPU Memory: {response["gpu_memory_total"]} bytes')
        print(f'Total Storage: {response["storage_total"]} bytes')
        print('-' * 80)

        return response["output"]
    except FileNotFoundError as e:
        print(e)
    except AttributeError as e:
        print(e)


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


def display_scores(score_df):
    for metric, scores in score_df.items():
        plt.bar(score_df.index, scores)
        plt.title(metric)
        plt.show()


def execute_pipeline(dataset_id: int, model_id: int, metric_id_list: list):
    # dataset
    dataset = Dataset(dataset_id)
    data = dataset.load()
    X = data.file1
    ground_truth = data.file2

    # model
    model = Model(model_id)
    result = model.execute(data=X)
    matrix = result.prediction

    # metrics
    metrics_names = []
    scores = []
    for metric_id in metric_id_list:
        metric = Metric(metric_id)
        result = metric.evaluate(ground_truth=ground_truth, prediction=matrix)
        metrics_names.append(metric.name)
        scores.append(result.score)

    return dataset.name, model.name, metrics_names, scores


def main():
    benchmark = [(0, 0, [0, 1]),
                 (0, 1, [0, 1])]

    dataset_model = []
    metric_names = []
    scores_list = []

    for pipeline in benchmark:
        dataset, model, metrics, scores = execute_pipeline(dataset_id=pipeline[0],
                                                           model_id=pipeline[1],
                                                           metric_id_list=pipeline[2])
        dataset_model.append(f'{dataset}_{model}')
        metric_names = metrics
        scores_list.append(scores)

    score_df = pd.DataFrame(scores_list, columns=metric_names, index=dataset_model)

    display_scores(score_df)


if __name__ == '__main__':
    main()
