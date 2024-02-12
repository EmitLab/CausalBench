import tigramite
import pandas
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr
import numpy

def execute(data, space):
    # check if `data` is dataframe
    if not isinstance(data, pandas.DataFrame):
        raise TypeError("data must be a DataFrame object")

    # the model does not take space, it should be type none.
    if not isinstance(space, None):
        raise TypeError("This model does not support space.")

    X = data
    pcmci = PCMCI(dataframe=X, cond_ind_test=ParCorr())
    result = pcmci.run_pcmci()
    pred_output = result['graph']
    p_matrix = result['p_matrix']

    # check if returned data type is graph/adjacency matrix
    if isinstance(pred_output, numpy.ndarray) or isinstance(pred_output, pandas.DataFrame):
        # Check if it's a square matrix for adjacency matrix
        if len(pred_output.shape) == 2 and pred_output.shape[0] == pred_output.shape[1]:
            print("result is an adjacency matrix")
        else:
            print("result is not an adjacency matrix")
    else:
        print("result is neither a numpy array nor a pandas DataFrame")

    #mapping pred_output graph to regular, checking for p values of < 0.05, null hypothesis
    result_array = numpy.logical_and(pred_output == '-->', p_matrix < 0.05).astype(int)


    return (result_array)
            #,'val_matrix': result['val_matrix'],
            #'p_matrix': result['p_matrix'],
            #'conf_matrix': result['conf_matrix']}