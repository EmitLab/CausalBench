import warnings
import numpy as np

from causalbench.formats import SpatioTemporalGraph


def evaluate(prediction: SpatioTemporalGraph, ground_truth: SpatioTemporalGraph, helpers: any, binarize: bool = True):
    # convert to adjacency matrix
    preds = helpers.graph_to_adjmatwlag(prediction)
    truths = helpers.graph_to_adjmatwlag(ground_truth)

    # align the adjacency matrices
    # this step make sure that the adjacency matrices match in shape, and have the same nodes
    preds, truths = helpers.align_adjmatswlag(preds, truths)

    print(len(preds), len(truths))

    score = 0
    for pred, truth in zip(preds, truths):
        # convert to numpy matrix
        pred = pred.to_numpy().astype(int)
        truth = truth.to_numpy().astype(int)

        # check if `truth` and `pred` are binary and binarize if necessary
        if not np.all(np.isin(truth, [0, 1])):
            if binarize:
                truth = (truth != 0).astype(int)
                warnings.warn("ground_truth has been binarized.")
            else:
                warnings.warn("ground_truth is not binary.")

        if not np.all(np.isin(pred, [0, 1])):
            if binarize:
                pred = (pred != 0).astype(int)
                warnings.warn("prediction has been binarized.")
            else:
                warnings.warn("prediction is not binary.")

        score += np.mean(pred == truth)

    # compute the average across the discovered causal graphs
    score /= len(truths)

    return {'score': score}
