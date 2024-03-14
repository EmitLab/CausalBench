import numpy as np
import pandas as pd

from causalbench.formats import SpatioTemporalGraph


def adjmat_to_graph(adjmat: np.ndarray, nodes: list[str], weight: str = 'strength') -> SpatioTemporalGraph:
    if weight not in ['strength', 'lag']:
        raise ValueError(f'Invalid type of weight: {weight}')

    data = []

    for index_cause, cause in enumerate(nodes):
        for index_effect, effect in enumerate(nodes):
            if weight == 'strength':
                if adjmat[index_cause, index_effect] != 0:
                    data.append((cause, effect, 0, 0, adjmat[index_cause, index_effect], 0))
            else:
                data.append((cause, effect, 0, 0, 0, adjmat[index_cause, index_effect]))

    columns = ['cause', 'effect', 'location_cause', 'location_effect', 'strength', 'lag']
    data = pd.DataFrame(data, columns=columns)

    graph = SpatioTemporalGraph(data)
    graph.index = {x: x for x in columns}

    return graph


def graph_to_adjmat(graph: SpatioTemporalGraph, weight: str = 'strength') -> pd.DataFrame:
    if weight not in ['strength', 'lag']:
        raise ValueError(f'Invalid type of weight: {weight}')

    nodes = graph.nodes
    adjmat = pd.DataFrame(0, columns=nodes, index=nodes)

    for index, (cause, effect, _, _, strength, lag) in graph.data.iterrows():
        if weight == 'strength':
            adjmat.loc[cause, effect] += strength
        else:
            adjmat.loc[cause, effect] = lag

    return adjmat


def temporal_log_to_graph(temporal_log: np.ndarray, cause: int, effect: int, lag: int) -> SpatioTemporalGraph:
    data = []

    for index, row_data in enumerate(temporal_log):
        data.append((row_data[cause], row_data[effect], 0, 0, row_data[lag], 0))

    columns = ['cause', 'effect', 'location_cause', 'location_effect', 'strength', 'lag']
    data = pd.DataFrame(data, columns=columns)

    return SpatioTemporalGraph(data, *columns)

def adjmatwlag_to_graph(adjmatWLag: np.ndarray, nodes: list[str]) -> SpatioTemporalGraph:
    data = []
    lag = 0
    for adjmat in adjmatWLag:
        for index_cause, cause in enumerate(nodes):
            for index_effect, effect in enumerate(nodes):
                if adjmat[index_cause, index_effect] != 0:
                    data.append((cause, effect, 0, 0, adjmat[index_cause, index_effect], lag))
        lag += 1

    columns = ['Cause', 'Effect', 'Location_Cause', 'Location_Effect', 'strength', 'lag']
    data = pd.DataFrame(data, columns=columns)
    print (data)
    return SpatioTemporalGraph(data, *columns)