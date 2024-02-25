import numpy as np
import pandas as pd

from formats import SpatioTemporalGraph


def adjmat_to_graph(adjmat: np.ndarray, nodes: list[str], weight: str = 'lag') -> SpatioTemporalGraph:
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
