import lingam
from causalbench.helpers.discovery import adjmatwlag_to_graph

def execute(data):

    X = data.data.drop(columns=data.time)

    model = lingam.VARLiNGAM()
    model.fit(X)

    result = model.adjacency_matrices_

    pred = adjmatwlag_to_graph(result, nodes=X.columns)

    return {'pred': pred}