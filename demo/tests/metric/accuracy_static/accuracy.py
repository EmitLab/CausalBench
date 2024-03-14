import numpy as np

from causalbench.formats import SpatioTemporalGraph
from causalbench.helpers.discovery import graph_to_adjmat


def evaluate(pred: SpatioTemporalGraph, truth: SpatioTemporalGraph):
    # convert to adjacency matrix
    pred = graph_to_adjmat(pred)
    truth = graph_to_adjmat(truth)

    # convert to numpy matrix
    pred = pred.to_numpy()
    truth = truth.to_numpy()

    # check if `truth` and `pred` have the same shape
    if truth.shape != pred.shape:
        raise ValueError("truth and pred must have the same shape")

    # check if `truth` and `pred` are binary
    if not np.all(np.isin(truth, [0, 1])):
        raise ValueError("truth must be binary")
    if not np.all(np.isin(pred, [0, 1])):
        raise ValueError("pred must be binary")
    
    score = np.mean(pred == truth)

    return {'score': score}
