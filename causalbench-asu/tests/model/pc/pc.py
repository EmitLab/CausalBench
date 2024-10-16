from castle.algorithms import PC


def execute(data, variant, alpha, ci_test, helpers: any):
    X = data.data

    pc = PC(variant=variant, alpha=alpha, ci_test=ci_test)

    pc.learn(X)

    prediction = helpers.adjmat_to_graph(pc.causal_matrix, nodes=data.data.columns)

    return {'prediction': prediction}
