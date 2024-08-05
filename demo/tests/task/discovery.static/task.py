import numpy as np
import pandas as pd

from causalbench.commons.helpers import adjmat_to_graph
from causalbench.formats import SpatioTemporalGraph, SpatioTemporalData
from causalbench.modules.task import AbstractTask


class DiscoveryStatic(AbstractTask):

    def helpers(self) -> any:
        return Helpers

    def model_data_inputs(self) -> dict[str, type]:
        return {'data': SpatioTemporalData}

    def metric_data_inputs(self) -> dict[str, type]:
        return {'ground_truth': SpatioTemporalGraph}

    def metric_model_inputs(self) -> dict[str, type]:
        return {'prediction': SpatioTemporalGraph}


class Helpers:

    @staticmethod
    def adjmat_to_graph(adjmat: np.ndarray, nodes: list[str], weight: str = 'strength') -> SpatioTemporalGraph:
        return adjmat_to_graph(adjmat, nodes, weight)

    @staticmethod
    def adjmatwlag_to_graph(adjmatWLag: np.ndarray, nodes: list[str]) -> SpatioTemporalGraph:
        data = []
        lag = 0
        for adjmat in adjmatWLag:
            for index_cause, cause in enumerate(nodes):
                for index_effect, effect in enumerate(nodes):
                    if adjmat[index_cause, index_effect] != 0:
                        data.append((cause, effect, 0, 0, adjmat[index_cause, index_effect], lag))
            lag += 1

        columns = ['cause', 'effect', 'location_cause', 'location_effect', 'strength', 'lag']
        data = pd.DataFrame(data, columns=columns)

        graph = SpatioTemporalGraph(data)
        graph.index = {x: x for x in columns}

        return graph

    @staticmethod
    def graph_to_adjmat(graph: SpatioTemporalGraph, weight: str = 'strength') -> pd.DataFrame:
        if weight not in ['strength', 'lag']:
            raise ValueError(f'Invalid type of weight: {weight}')

        nodes = graph.nodes
        adjmat = pd.DataFrame(0.0, columns=nodes, index=nodes)

        for index, row in graph.data.iterrows():
            cause = row[graph.cause]
            effect = row[graph.effect]

            if weight == 'strength':
                strength = row[graph.strength]
                adjmat.at[cause, effect] += strength
            else:
                lag = row[graph.lag]
                adjmat.at[cause, effect] = lag

        return adjmat

    @staticmethod
    def align_adjmats(adjmat1: pd.DataFrame, adjmat2: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
        nodes = sorted(set(adjmat1.columns.tolist() + adjmat2.columns.tolist()))

        aligned_adjmat1 = pd.DataFrame(index=nodes, columns=nodes)
        aligned_adjmat2 = pd.DataFrame(index=nodes, columns=nodes)

        for cause in nodes:
            for effect in nodes:
                if cause in adjmat1.index and effect in adjmat1.columns:
                    aligned_adjmat1.at[cause, effect] = adjmat1.at[cause, effect]
                else:
                    aligned_adjmat1.at[cause, effect] = 0

                if cause in adjmat2.index and effect in adjmat2.columns:
                    aligned_adjmat2.at[cause, effect] = adjmat2.at[cause, effect]
                else:
                    aligned_adjmat2.at[cause, effect] = 0

        return aligned_adjmat1, aligned_adjmat2
