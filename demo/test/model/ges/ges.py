from castle.algorithms.ges.ges import GES


def execute(data, space):
    X = data
    
    ges = GES()
    ges.learn(X)

    return {'pred': ges.causal_matrix}
