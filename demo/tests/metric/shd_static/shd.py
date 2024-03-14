"""
SHD depends on the definition of adjacency matrix, i.e how to handle undirected edges, reversed edges.
For now, we do not differentiate reversed edges and undirected edges.
"""

import numpy as np
import pandas as pd

from causalbench.formats import SpatioTemporalGraph
from causalbench.helpers.discovery import graph_to_adjmat


def evaluate(pred: SpatioTemporalGraph, truth: SpatioTemporalGraph):
    r"""Compute the Structural Hamming Distance.

    Args:
        pred (numpy.ndarray): Predicted adjacency matrix, must be of 
            ones and zeros.
        truth (numpy.ndarray): Ground truth adjacency matrix, must be of the same shape as `pred`.

    Examples:
        >>> from numpy.random import randint
        >>> pred, truth = randint(2, size=(10, 10)), randint(2, size=(10, 10))
        >>> SHD(pred, truth)
    """
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

    # compute the SHD
    diff = np.abs(truth - pred)
    score = np.sum(diff)

    return {'score': score}
