import numpy as np
import pandas as pd
from typing import List
import warnings

from causalbench.formats import SpatioTemporalGraph, SpatioTemporalData
from causalbench.modules.task import AbstractTask


class DiscoveryTemporal(AbstractTask):

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
    def graph_to_adjmatwlag(graph: SpatioTemporalGraph) -> List[pd.DataFrame]:
        # transform SpatioTemporalGraph back to a list of adjacency matrices
        nodes = graph.nodes
        adjmats = []
        lags = list(range(graph.data[graph.lag].min(), graph.data[graph.lag].max() + 1))

        for lag in lags:
            adjmat = pd.DataFrame(0.0, columns=nodes, index=nodes)
            # if a lag is not in the data, the adjacency matrix is all zeros
            if lag not in graph.data[graph.lag].values:
                adjmats.append(adjmat)
                continue
            for index, row in graph.data[graph.data[graph.lag] == lag].iterrows():
                cause = row[graph.cause]
                effect = row[graph.effect]
                if graph.strength is None:
                    strength = 1
                else:
                    strength = row[graph.strength]
                adjmat.at[cause, effect] = strength
            adjmats.append(adjmat)

        return adjmats

    @staticmethod
    def align_adjmatswlag(adjmats1: List[pd.DataFrame], adjmats2: List[pd.DataFrame]) -> (List[pd.DataFrame], List[pd.DataFrame]):
        # This function fix the issue when the nodes are not the same in two list of adjacency matrices
        # Example:
        # adjmats1 has node A, B, C
        # adjmats2 has node A, B, D
        # The function will return two adjacency matrices with nodes A, B, C, D

        # check if the length of the two lists of adjacency matrices are the same
        if len(adjmats1) != len(adjmats2):
            warnings.warn("The number of adjacency matrices must be the same")
            # NOTE: add 0 adjacency matrices so that the length of the two lists are the same
            # find the one with less adjacency matrices
            diff = abs(len(adjmats1) - len(adjmats2))
            if len(adjmats1) < len(adjmats2):
                for _ in range(diff):
                    adjmats1.append(pd.DataFrame(0, columns=adjmats1[0].columns, index=adjmats1[0].index))
            else:
                for _ in range(diff):
                    adjmats2.append(pd.DataFrame(0, columns=adjmats2[0].columns, index=adjmats2[0].index))

        # for each list of adjacency matrices, get all nodes
        nodes = sorted(set([node for adjmat in adjmats1 for node in adjmat.columns] + [node for adjmat in adjmats2 for node in adjmat.columns]))

        aligned_adjmats1 = []
        aligned_adjmats2 = []

        for adjmat1, adjmat2 in zip(adjmats1, adjmats2):
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
            aligned_adjmats1.append(aligned_adjmat1)
            aligned_adjmats2.append(aligned_adjmat2)

        return aligned_adjmats1, aligned_adjmats2
