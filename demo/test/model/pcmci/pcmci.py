import tigramite
import pandas
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr

def execute(data):

    # check if `data` is dataframe
    if not isinstance(data, pandas.dataframe.DataFrame):
        raise TypeError("data must be a DataFrame object")

    X = data
    pcmci = PCMCI(dataframe=X, cond_ind_test=ParCorr)
    result = pcmci.run_pcmci()

    return ({'pred': result['graph']})
            #,'val_matrix': result['val_matrix'],
            #'p_matrix': result['p_matrix'],
            #'conf_matrix': result['conf_matrix']}