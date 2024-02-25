import numpy as np
import pandas as pd

from causalbench.formats import SpatioTemporalGraph


def adjmat_to_graph(adjmat: np.ndarray, nodes: list[str], weight: str = 'strength') -> SpatioTemporalGraph:
    if weight not in ['lag', 'strength']:
        raise ValueError(f'Invalid type of weight: {weight}')

    data = []

    for index_cause, cause in enumerate(nodes):
        for index_effect, effect in enumerate(nodes):
            if weight == 'lag':
                data.append((cause, effect, 0, 0, adjmat[index_cause, index_effect], 0))
            else:
                data.append((cause, effect, 0, 0, 0, adjmat[index_cause, index_effect]))

    columns = ['Cause', 'Effect', 'Location_Cause', 'Location_Effect', 'Lag', 'Strength']
    data = pd.DataFrame(data, columns=columns)

    return SpatioTemporalGraph(data, *columns)


def graph_to_adjmat(graph: SpatioTemporalGraph, weight: str = 'strength') -> pd.DataFrame:
    if weight not in ['lag', 'strength']:
        raise ValueError(f'Invalid type of weight: {weight}')

    nodes = graph.nodes
    adjmat = pd.DataFrame(0, columns=nodes, index=nodes)

    for index, (cause, effect, _, _, lag, strength) in graph.data.iterrows():
        if weight == 'lag':
            adjmat.loc[cause, effect] = lag
        else:
            adjmat.loc[cause, effect] += strength

    return adjmat


def temporal_log_to_graph(temporal_log: np.ndarray, cause: int, effect: int, lag: int) -> SpatioTemporalGraph:
    data = []

    for index, row_data in enumerate(temporal_log):
        data.append((row_data[cause], row_data[effect], 0, 0, row_data[lag], 0))

    columns = ['Cause', 'Effect', 'Location_Cause', 'Location_Effect', 'Lag', 'Strength']
    data = pd.DataFrame(data, columns=columns)

    return SpatioTemporalGraph(data, *columns)
