import numpy as np


def evaluate(pred, truth):
    truth = truth.to_numpy()

    # check if `truth` and `pred` are numpy arrays
    if not isinstance(truth, np.ndarray):
        raise TypeError("truth must be a numpy.ndarray")
    if not isinstance(pred, np.ndarray):
        raise TypeError("pred must be a numpy.ndarray")

    # check if `truth` and `pred` have the same shape
    assert(pred.shape==truth.shape and pred.shape[0]==pred.shape[1])

    # check if `truth` and `pred` are binary
    if not np.all(np.isin(truth, [0, 1])):
        raise ValueError("truth must be binary")
    if not np.all(np.isin(pred, [0, 1])):
        raise ValueError("pred must be binary")

    TP = np.sum((pred + truth) == 2)
    TP_FP = pred.sum(axis=1).sum()
    TP_FN = truth.sum(axis=1).sum()
    precision = TP/TP_FP
    recall = TP/TP_FN
    score = 2*(recall*precision)/(recall+precision)

    return {'score': score}
