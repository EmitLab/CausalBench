import pandas as pd
import lingam

# Load the dataset
df = pd.read_csv('C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/data/Telecom/real_dataset_processed.csv')

# Drop the 'timestep' column as it's not part of the data for causal discovery
df = df.drop(columns=["timestep"], errors="ignore")

# Print the first few rows to check the data
print(df.head())
print()

# Perform causal discovery using VARLiNGAM
model = lingam.VARLiNGAM()
model.fit(df)

for index, adj_matrix in enumerate(model.adjacency_matrices_):
    # Convert the adjacency matrix to a pandas DataFrame with proper labels
    adj_df = pd.DataFrame(adj_matrix, index=df.columns, columns=df.columns)
    adj_df[adj_df != 0] = 1
    adj_df.to_csv(f'adjmat{index}.csv', index=True)
