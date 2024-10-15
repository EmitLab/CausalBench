from castle.algorithms import PC


def execute(data, alpha, helpers: any):
    X = data.data

    pc = PC()
    pc.learn(X)

    prediction = helpers.adjmat_to_graph(pc.causal_matrix, nodes=data.data.columns)

    return {'prediction': prediction}
