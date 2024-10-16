from castle.algorithms.ges.ges import GES


def execute(data, criterion, method, k, N, helpers: any):
    X = data.data
    
    ges = GES(criterion=criterion, method=method, k=k, N=N)
    ges.learn(X)

    prediction = helpers.adjmat_to_graph(ges.causal_matrix, nodes=X.columns)

    return {'prediction': prediction}
