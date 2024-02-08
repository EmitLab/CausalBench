import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from commons import executor
from modules.pipeline import Pipeline


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


# def display_scores(score_df):
#     for metric, scores in score_df.items():
#         plt.bar(score_df.index, scores)
#         plt.title(metric)
#         plt.show()


def main():
    pipeline0 = Pipeline(0)
    result0 = pipeline0.execute()
    print(result0.metrics)

    pipeline1 = Pipeline()
    pipeline1.create(name='pipeline1',
                     task='discovery',
                     dataset=0,
                     model=(1, {'data': 'file1'}),
                     metrics=[(0, {'ground_truth': 'file2'}),
                              (1, {'ground_truth': 'file2'})])
    result1 = pipeline1.execute()
    print(result1.metrics)
    # pipeline1.publish()


if __name__ == '__main__':
    main()
