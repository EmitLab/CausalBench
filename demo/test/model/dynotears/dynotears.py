from causalnex.structure import StructureModel
from causalnex.structure import dynotears
from causalnex.structure.dynotears import from_pandas_dynamic
import pandas
import numpy
def execute(data, space):
    # check if `data` is dataframe
    if not isinstance(data, pandas.DataFrame):
        raise TypeError("data must be a DataFrame object")

    # the model does not take space, it should be type none.
    if space is not None:
        raise TypeError("This model does not support space.")

    sm = from_pandas_dynamic(data, p=1)
        #P may need to be adjusted as it is
        #"Number of past interactions we allow the model to create. "

    pred_output = sm.edges
        #TODO this returns a string list of pairs, needs to be convered to adjmatrix.

    # check if returned data type is graph/adjacency matrix
    if isinstance(pred_output, numpy.ndarray) or isinstance(pred_output, pandas.DataFrame):
        # Check if it's a square matrix for adjacency matrix
        if len(pred_output.shape) == 2 and pred_output.shape[0] == pred_output.shape[1]:
            print("result is an adjacency matrix")
        else:
            print("result is not an adjacency matrix")
    else:
        print("result is neither a numpy array nor a pandas DataFrame")

    return {'pred': sm.edges}