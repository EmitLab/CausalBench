import numpy as np


def evaluate(pred, truth):
    
    # check if pred is a 2d numpy array
    if pred.shape[0] == pred.shape[1]:
        d = pred.shape[0]
        total = 0.5 * d * (d - 1)
        TP = np.sum((pred + truth) == 2)
        FP = np.sum((pred == 1) & (truth == 0)) 
        TN = total - FP
    # TODO: need to find a uniqe condition
    # claculate total number of edges as 
    if True:
        np.array_equal(pred, truth)
        total = 0.5 * d * (d - 1)
        TP = np.sum((pred + truth) == 2, axis=0)
        FP = np.sum((pred == 1) & (truth == 0), axis=0)
        TN = total - FP
    score = (TP + TN) / total

    return {'score': score}
