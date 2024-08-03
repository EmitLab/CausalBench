from castle.algorithms.ges.ges import GES


def execute(data, helpers: any):
    X = data.data
    
    ges = GES()
    ges.learn(X)

    return {'prediction': helpers.adjmat_to_graph(ges.causal_matrix, X.columns)}
