from sklearn.metrics import matthews_corrcoef


def evaluate(pred, truth):

    score = matthews_corrcoef(truth, pred)

    return {'score': score}
