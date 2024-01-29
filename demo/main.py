import logging

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

import executor
from datasetReader import read_dataset


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


def plot_graph(matrix, nodes):
    plt.figure(figsize=(10, 6))

    rows, cols = np.where(matrix == 1)
    edges = zip(rows.tolist(), cols.tolist())
    labels = {i: label for i, label in enumerate(nodes)}

    graph = nx.DiGraph()
    graph.add_nodes_from(range(len(nodes)))
    graph.add_edges_from(edges)

    pos = nx.arf_layout(graph)
    nx.draw_networkx_nodes(graph, pos,
                           node_size=[len(labels[i]) * 500 for i in graph.nodes],
                           node_color='white',
                           edgecolors='black')
    nx.draw_networkx_edges(graph, pos,
                           node_size=[len(labels[i]) * 500 for i in graph.nodes])
    nx.draw_networkx_labels(graph, pos, labels)

    plt.axis('off')
    plt.tight_layout()
    plt.show()


def main():
    # disable logging
    logger = logging.getLogger()
    logger.disabled = True

    # dataset
    # X = pd.read_csv('./data/abalone.mixed.numeric.txt', delim_whitespace=True)
    dataframes = read_dataset()
    X = dataframes[0]
    ground_truth = dataframes[1]

    # model
    matrix = execute_and_report("./model1.py", "execute", data=[X], space=None)

    # metrics
    score = execute_and_report("./metric1.py", "SHD", pred=matrix, truth=ground_truth)
    print(f'SHD score: {score}')

    # visualize
    plot_graph(matrix, X.columns.tolist())
    plot_graph(ground_truth.values, X.columns.tolist())


if __name__ == '__main__':
    main()
