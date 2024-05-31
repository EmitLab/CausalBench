from castle.algorithms.ges.ges import GES

from causalbench.helpers.discovery import adjmat_to_graph


def execute(data):
    X = data.data
    
    ges = GES()
    ges.learn(X)

    return {'pred': adjmat_to_graph(ges.causal_matrix, X.columns)}
