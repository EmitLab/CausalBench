import pandas as pd
from causalbench.modules.task import Task

df1 = pd.read_csv('C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/causal_info_adjmat.csv', index_col=0)
# df2 = pd.read_csv('C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/adjmat1.csv', index_col=0)
arr = [df1.to_numpy()]

task = Task('discovery.temporal').load()
graph = task.helpers().adjmatwlag_to_graph(arr, df1.columns.tolist())

graph.data.to_csv(f'graph.csv', index=False)
