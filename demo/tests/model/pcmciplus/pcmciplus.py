import numpy as np
from tigramite.independence_tests.parcorr import ParCorr
from tigramite.pcmci import PCMCI
from tigramite import data_processing as pp

def execute(data, helpers: any):
    X = data.data.drop(columns=data.time)
    X_processed = pp.DataFrame(X.to_numpy())
    pcmci = PCMCI(dataframe=X_processed,
                  cond_ind_test=ParCorr(significance='analytic'))
    results = pcmci.run_pcmciplus(tau_min=0, tau_max=2)
    graphs = results['graph']

    # transform the graph to adjmatwlag format
    n, m, tau = graphs.shape
    result = np.zeros((n, m, tau), dtype=int)
    for i in range(n):
        for j in range(m):
            for t in range(tau):
                if graphs[i, j, t] == '-->':
                    result[i, j, t] = 1
                elif graphs[i, j, t] == '<--':
                    result[i, j, t] = 0
                    result[j, i, t] = 1


    adjmatwlag = [np.zeros((n, m), dtype=int) for _ in range(tau)]

    for t in range(tau):
        for i in range(n):
            for j in range(m):
                if result[i, j, t] == 1:
                    adjmatwlag[t][i, j] = 1

    # Transform the result array to a list of tau-length (n, m) arrays
    prediction = helpers.adjmatwlag_to_graph(adjmatwlag, nodes=X.columns)

    # should return prediction instead
    return {'prediction': prediction}