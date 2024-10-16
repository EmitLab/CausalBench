import numpy as np
from tigramite.independence_tests.parcorr import ParCorr
from tigramite.pcmci import PCMCI
from tigramite import data_processing as pp

def execute(data, tau_min, tau_max, pc_alpha,
            contemp_collider_rule, conflict_resolution, reset_lagged_links,
            max_conds_dim, max_combinations, max_conds_py, max_conds_px,
            max_conds_px_lagged, fdr_method, helpers: any):
    X = data.data.drop(columns=data.time)
    X_processed = pp.DataFrame(X.to_numpy())

    pcmci = PCMCI(dataframe=X_processed, cond_ind_test=ParCorr(significance='analytic'))

    results = pcmci.run_pcmciplus(tau_min=tau_min, tau_max=tau_max,
                                  pc_alpha=pc_alpha,
                                  contemp_collider_rule=contemp_collider_rule,
                                  conflict_resolution=conflict_resolution,
                                  reset_lagged_links=reset_lagged_links,
                                  max_conds_dim=max_conds_dim,
                                  max_combinations=max_combinations,
                                  max_conds_py=max_conds_py,
                                  max_conds_px=max_conds_px,
                                  max_conds_px_lagged=max_conds_px_lagged,
                                  fdr_method=fdr_method)
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