import numpy
import pandas

import lingam


def execute(data, space):

    # check if `data` is dataframe
    if not isinstance(data, pandas.DataFrame):
        raise TypeError("data must be a DataFrame object")

    # the model does not take space, it should be type none.
    if not isinstance(space, None):
        raise TypeError("This model does not support space.")

    X = data
    model = lingam.DirectLiNGAM()
    model.fit(X)

    pred_output = model.adjacency_matrix_

    # check if returned data type is graph/adjacency matrix
    if isinstance(pred_output, numpy.ndarray) or isinstance(pred_output, pandas.DataFrame):
        # Check if it's a square matrix for adjacency matrix
        if len(pred_output.shape) == 2 and pred_output.shape[0] == pred_output.shape[1]:
            print("result is an adjacency matrix")
        else:
            print("result is not an adjacency matrix")
    else:
        print("result is neither a numpy array nor a pandas DataFrame")

    return {'pred': model.adjacency_matrix_}