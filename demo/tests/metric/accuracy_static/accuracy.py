import numpy as np
import pandas as pd


def evaluate(pred, truth):
    # check if `truth` and `pred` are pandas DataFrames
    if not isinstance(pred, pd.DataFrame):
        raise TypeError("pred must be a pandas DataFrame")
    if not isinstance(truth, pd.DataFrame):
        raise TypeError("truth must be a pandas DataFrame")

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
