# Causal Bench

## Evaluation
Evaluate graph structure
Evaluate causal mechanism

Prediction-based metrics
These metrics are to measure the accuracy
MSE, MRSE, CPRS
- input: dataframe
- output: decimal

Graph-based metrics: Accuracy, recall, precision, F1, SHD
- input: graph
- output: decimal

> Only consider fully identified DAGs, (not considering DAGs with un-oriented edges such as CPDAGs, PDAGs)

### Static Causal Discovery
#### Dataframe format:
| $X_1$ | $X_2$ | $X_3$ |
|----------|------|-----|
|   ..   | .. | ..  |
|  ..    |.. | ..  |

A dataframe with n columns, each column represents a feature/attributes, and each row represents a sample.

####Graph format:
Causal DAGs is transcribed into an adjacency matrix $\mathbf{A}$.
Adjacency matrix $\mathbf{A}$ is a 2-d square matrix. Each row and column represents a feature/attribute. The value of $\mathbf{A}[i, j]$ is 1 if there is a directed edge from $i$ to $j$, otherwise 0.

$$
\mathbf{A}[i, j] = \begin{cases}
1 & \text{if } i \rightarrow j \\
0 & \text{if no causal relationship} \\
\end{cases}
$$

#### reference
gcastcle

### Temporal Causal Discovery
#### Dataframe format:
| Time | $X_1$ | $X_2$ |
| --- | --- | --- |
| 1  | ..  | ..  |
| 2  | ..  | ..  |

A dataframe with $n + 1$ columns, the first column represents the time index, and the rest n columns represent features/attributes. Each row represents a sample at a specific time.

or

| $X_1$ | $X_2$ | $X_3$ |
| ---- | ----- | ----- |
| ...    | ...    | ..    |
| ...    | ...    | ..    |

A dataframe like the static causal discovery, but each column is a time series of a feature/attribute.
Time index is implicit.

#### Graph format:
Temporal causal DAGs has an additional lag attribute compared to static causal DAGs. The adjacency graph $\mathbf{A}$ is a 3-dimensional dataframe.

$$A_i = [c, e, \tau]$$
- $c, e$: cause and effect
- $\tau$: lag, 0 is allowed for instantaneous causality (optional?)
- self-loop is forbidden ($A[c, c, 0] = 0$)
- feedback loop with $\tau > 0$ is allowed

or in Dict format
```python
{
 'j1': {('c1', 1): 'r1', ('c2', 2): 'r2', ('c3', 3): 'r3'},
 'j2': {('c1', 1): 'r1', ('c2', 2): 'r2', ('c3', 3): 'r3'},
 'j3': {('c1', 1): 'r1', ('c2', 2): 'r2', ('c3', 3): 'r3'}
}
```

Classification metrics can be grouped in several 
1. on any relationships
2. on lagged relationships
3. on contemporaneous relationships
4. cause identification only

Only compare existence, not penalize on the value.