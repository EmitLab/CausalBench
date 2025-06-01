import numpy as np
import pandas as pd
import networkx as nx
from dowhy import CausalModel, gcm
from econml.dml import CausalForestDML
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import HistGradientBoostingRegressor
from causalbench.modules import Run

import warnings

warnings.filterwarnings('ignore')



def compute_CATE(data, treatment, outcome, graph):
    model = CausalModel(
        data=data,
        treatment=treatment,
        outcome=outcome,
        graph = graph
    )

    identified_estimand = model.identify_effect()

    estimate = model.estimate_effect(
        identified_estimand,
        method_name='backdoor.linear_regression',
        test_significance=True
    )

    return estimate.value


def compute_score(data):
    data = data.drop(columns=['dataset'], axis=1)

    G = nx.DiGraph()
    for hyperparameter in hyperparameters:
        for metric in metrics.keys():
            G.add_edge(hyperparameter, metric)

    scores = np.zeros(shape=(len(hyperparameters), len(metrics)))
    scores = pd.DataFrame(scores, index=hyperparameters, columns=list(metrics.keys()))

    for hyperparameter in hyperparameters:
        for metric in metrics.keys():
            scores.loc[hyperparameter, metric] = compute_CATE(data, hyperparameter, metric, G)

    return scores



""" VAR-LiNGAM """
# run: Run = Run(module_id=59)
# hyperparameters = ['criterion', 'prune']
# encode = [0, 1]
# metrics = {'accuracy': 'accuracy_temporal',
#            'precision': 'precision_temporal',
#            'recall': 'recall_temporal',
#            'f1': 'f1_temporal',
#            'SHD': 'SHD_temporal'}

""" PCMCI+ """
run: Run = Run(module_id=63)
hyperparameters = ['alpha', 'max_conds_dim']
encode = []
metrics = {'accuracy': 'accuracy_temporal',
           # 'precision': 'precision_temporal',
           # 'recall': 'recall_temporal',
           'f1': 'f1_temporal',
           'SHD': 'SHD_temporal'}

""" PC """
# run: Run = Run(module_id=62)
# hyperparameters = ['alpha', 'variant']
# encode = [1]
# metrics = {'accuracy': 'accuracy_static',
#            # 'precision': 'precision_static',
#            # 'recall': 'recall_static',
#            'f1': 'f1_static'}



df = pd.DataFrame(columns=['dataset'] + hyperparameters + list(metrics.keys()))
for index, result in enumerate(run.results):
    row = []

    row.append(result.dataset.name)

    for hyperparameter in hyperparameters:
        row.append(result.model.hyperparameters[hyperparameter])

    curr_metrics = {metric.name: float(metric.output.score) for metric in result.metrics}
    for metric, name in metrics.items():
        row.append(curr_metrics[name])

    df.loc[index] = row

for index, hyperparameter in enumerate(hyperparameters):
    if index in encode:
        label_encoder = LabelEncoder()
        df[hyperparameter] = label_encoder.fit_transform(df[hyperparameter])
        print(label_encoder.classes_)

print(df)
print()
print()

dfx = df[df['dataset'] == 'Short-term electricity load forecasting (Panama)']
dfx = dfx.drop(columns=['dataset'], axis=1)
print(dfx)
# dfx['variant'] = df['variant'].map(dict(enumerate(['original', 'stable'])))
# dfx = dfx.iloc[[0, 1, 20, 21, 38, 39]]
# print(dfx.to_latex(float_format='%.4f', index=False))
print(dfx.sample(8, random_state=42).sort_index())
print(dfx.sample(8, random_state=42).sort_index().to_latex(float_format='%.4f', index=True))
print()
print()

dfs = {key: group for key, group in df.groupby('dataset')}

for dataset, data in dfs.items():
    score = compute_score(data)

    print(f'[{dataset}]')
    print(score.to_latex(float_format='%.4f'))
    print()
    print()
