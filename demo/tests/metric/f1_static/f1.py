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
    FP = np.sum((pred == 1) & (truth == 0))
    FN = np.sum((pred == 0) & (truth == 1))

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {'score': score}
