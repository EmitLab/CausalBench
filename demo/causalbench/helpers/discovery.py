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

def adjmatwlag_to_graph(adjmatWLag: np.ndarray, nodes: list[str], weight: str = 'strength') -> SpatioTemporalGraph:
    if weight not in ['strength']:
        raise ValueError(f'Invalid type of weight: {weight}')

    data = []
    lag = 0
    for adjmat in adjmatWLag:
        for index_cause, cause in enumerate(nodes):
            for index_effect, effect in enumerate(nodes):
                data.append((cause, effect, 0, 0, lag, adjmat[index_cause, index_effect]))
        lag += 1

    columns = ['Cause', 'Effect', 'Location_Cause', 'Location_Effect', 'Lag', 'Strength']
    data = pd.DataFrame(data, columns=columns)
    print (data)
    return SpatioTemporalGraph(data, *columns)
