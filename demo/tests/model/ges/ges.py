from castle.algorithms.ges.ges import GES


def execute(data):
    X = data.data
    
    ges = GES()
    ges.learn(X)

    return {'pred': ges.causal_matrix}
