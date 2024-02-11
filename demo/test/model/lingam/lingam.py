import pandas
import lingam

def execute(data):

    # check if `data` is dataframe
    if not isinstance(data, pandas.DataFrame):
        raise TypeError("data must be a DataFrame object")

    X = data
    model = lingam.DirectLiNGAM()
    model.fit(X)

    return {'pred': model.adjacency_matrix_}