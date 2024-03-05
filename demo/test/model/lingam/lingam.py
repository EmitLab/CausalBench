import pandas
import lingam
import numpy

def execute(data, space):

    # check if `data` is dataframe
    if not isinstance(data, pandas.DataFrame):
        raise TypeError("data must be a DataFrame object")

    # the model does not take space, it should be type none.
    if space is not None:
    #if not isinstance(space, None):
        raise TypeError("This model does not support space.")

    X = data
    model = lingam.VARLiNGAM()
    model.fit(X)

    pred_output = model._adjacency_matrices

    # check if returned data type is graph/adjacency matrix
    if isinstance(pred_output, numpy.ndarray) or isinstance(pred_output, pandas.DataFrame):
        # Check if it's a square matrix for adjacency matrix
        if len(pred_output.shape) == 2 and pred_output.shape[0] == pred_output.shape[1]:
            print("result is an adjacency matrix")
        else:
            print("result is not an adjacency matrix")
    else:
        print("result is neither a numpy array nor a pandas DataFrame")

    #print (model._adjacency_matrices)
    #print(model._adjacency_matrices.shape)
    #convert it into i, j, tau array and return it as such.
    result = model._adjacency_matrices
    result[result != 0] = 1

    #result is returned as an ndarray [time,i,j]
    return {'pred': result}