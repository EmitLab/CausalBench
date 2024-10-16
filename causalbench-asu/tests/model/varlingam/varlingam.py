import lingam
import numpy as np

def execute(data, lags, criterion, prune, random_state, helpers: any):

    X = data.data.drop(columns=data.time)

    model = lingam.VARLiNGAM(lags=lags, criterion=criterion, prune=prune, random_state=random_state)
    model.fit(X)

    order = model.causal_order_
    result = model.adjacency_matrices_
    # re-order the adjacency matrices based on the causal order
    for i, adjmat in enumerate(result):
        result[i] = adjmat[:, np.argsort(order)]
    prediction = helpers.adjmatwlag_to_graph(result, nodes=X.columns)
    return {'prediction': prediction}