import numpy as np
import warnings

from causalbench.formats import SpatioTemporalGraph
from causalbench.helpers.discovery import graph_to_adjmat

def evaluate(pred: SpatioTemporalGraph, truth: SpatioTemporalGraph, binarize: bool = True):

    # convert to adjacency matrix
    pred = graph_to_adjmat(pred)
    truth = graph_to_adjmat(truth)

    # convert to numpy matrix
    pred = pred.to_numpy()
    truth = truth.to_numpy()

    # check if `truth` and `pred` have the same shape
    if truth.shape != pred.shape:
        raise ValueError("truth and pred must have the same shape")

    # check if `truth` and `pred` are binary and binarize if necessary
    if not np.all(np.isin(truth, [0, 1])):
        if binarize:
            truth = (truth != 0).astype(int)
            warnings.warn("truth has been binarized.")
        else:
            raise ValueError("truth must be binary.")

    if not np.all(np.isin(pred, [0, 1])):
        if binarize:
            pred = (pred != 0).astype(int)
            warnings.warn("pred has been binarized.")
        else:
            raise ValueError("truth must be binary.")
    
    TP = np.sum((pred + truth) == 2)
    FN = np.sum((pred == 0) & (truth == 1))

    score = TP / (TP + FN) if (TP + FN) > 0 else 0

    return {'score': score}
