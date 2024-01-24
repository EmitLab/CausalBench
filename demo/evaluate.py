import numpy as np
from castle.metrics import MetricsDAG

def evaluate(B_est, B_true):
    m = MetricsDAG(B_est, B_true)
    print(m.metrics)

    return m.metrics

# Example usage
# matrix1 = np.array([[0, 1], [0, 0]])
# matrix2 = np.array([[1, 1], [0, 0]])
# res = evaluate(matrix1, matrix2)
# print(res)
