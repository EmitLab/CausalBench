import numpy as np

from causalbench.formats import SpatioTemporalGraph
from causalbench.helpers.discovery import graph_to_adjmat


def evaluate(pred: SpatioTemporalGraph, truth: SpatioTemporalGraph):

    # convert to adjacency matrix
    pred = graph_to_adjmat(pred, weight='lag')
    truth = graph_to_adjmat(truth, weight='lag')

    # convert to numpy matrix
    pred = pred.to_numpy().astype(int)
    truth = truth.to_numpy().astype(int)

    # check if `truth` and `pred` have the same shape
    if truth.shape != pred.shape:
        raise ValueError("truth and pred must have the same shape")

    # check if `truth` and `pred` are natural numbers
    if not (np.all(truth >= 0)):
        raise ValueError("truth must be natural numbers")

    if not (np.all(pred >= 0)):
        raise ValueError("pred must be natural numbers")

    # compute the SHD
    diff = np.abs(truth - pred)
    score = np.sum(diff)

    return {'score': score}
