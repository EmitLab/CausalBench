import pandas
import lingam
import numpy
from causalbench.helpers.discovery import adjmat_to_graph, adjmatwlag_to_graph


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

    result = model._adjacency_matrices
    result[result != 0] = 1 #Convert to adj matrix.

    print("Lingam returns an adjacency matrix for each lag, conformance checking the sub adj matrices...")
    for subArr in result:
        # check if returned data type is graph/adjacency matrix
        if isinstance(subArr, numpy.ndarray) or isinstance(subArr, pandas.DataFrame):
            # Check if it's a square matrix for adjacency matrix
            if len(subArr.shape) == 2 and subArr.shape[0] == subArr.shape[1]:
                print("result is an adjacency matrix")
            else:
                print("result is not an adjacency matrix")
        else:
            print("result is neither a numpy array nor a pandas DataFrame")


    pred = adjmatwlag_to_graph(result, nodes=data.columns)

    #print (model._adjacency_matrices)
    #print(model._adjacency_matrices.shape)

    #result is returned as an ndarray [lag,i,j]
    return {'pred': result}