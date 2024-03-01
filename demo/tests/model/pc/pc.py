from castle.algorithms import PC

from causalbench.helpers.discovery import adjmat_to_graph


def execute(data):
    X = data.data

    pc = PC()
    pc.learn(X)

    prediction = adjmat_to_graph(pc.causal_matrix, nodes=data.data.columns)

    return {'pred': prediction}
