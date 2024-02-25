import numpy as np


def evaluate(pred, truth):
    truth = truth.to_numpy()

    # check if `truth` and `pred` are numpy arrays
    if not isinstance(truth, np.ndarray):
        raise TypeError("truth must be a numpy.ndarray")
    if not isinstance(pred, np.ndarray):
        raise TypeError("pred must be a numpy.ndarray")

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
