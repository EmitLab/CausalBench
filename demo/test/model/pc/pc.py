from castle.algorithms import PC


def execute(data, space):
    X = data

    pc = PC()
    pc.learn(X)

    return {'pred': pc.causal_matrix}
