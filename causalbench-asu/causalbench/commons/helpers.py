import numpy as np
import pandas as pd

from causalbench.formats import SpatioTemporalGraph


def adjmat_to_graph(adjmat: np.ndarray, nodes: list[str], weight: str = 'strength') -> SpatioTemporalGraph:
    if weight not in ['strength', 'lag']:
        raise ValueError(f'Invalid type of weight: {weight}')

    data = []

    for index_cause, cause in enumerate(nodes):
        for index_effect, effect in enumerate(nodes):
            if adjmat[index_cause, index_effect] != 0:
                if weight == 'strength':
                    data.append((cause, effect, 0, 0, adjmat[index_cause, index_effect], 0))
                else:
                    data.append((cause, effect, 0, 0, 0, adjmat[index_cause, index_effect]))

    columns = ['cause', 'effect', 'location_cause', 'location_effect', 'strength', 'lag']
    data = pd.DataFrame(data, columns=columns)

    graph = SpatioTemporalGraph(data)
    graph.index = {x: x for x in columns}

    return graph
