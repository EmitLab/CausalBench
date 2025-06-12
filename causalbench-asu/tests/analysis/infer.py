import numpy as np
import pandas as pd
import networkx as nx
from dowhy import CausalModel, gcm
from econml.dml import CausalForestDML
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from yaml_to_csv import main as process_yaml_data, headers
import yaml
import requests
import os
import tempfile
from urllib.parse import urlparse

import warnings
warnings.filterwarnings('ignore')


def download_zip_from_url(url, download_dir):
    try:
        print(f"Downloading {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename or not filename.endswith('.zip'):
            filename = f"downloaded_{hash(url) % 10000}.zip"
        
        filepath = os.path.join(download_dir, filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {filename}")
        return filepath
        
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None


def fetch_zip_files(zip_urls, download_dir):
    downloaded_files = []
    
    os.makedirs(download_dir, exist_ok=True)
    
    for url in zip_urls:
        filepath = download_zip_from_url(url, download_dir)
        if filepath:
            downloaded_files.append(filepath)
    
    print(f"Successfully downloaded {len(downloaded_files)}/{len(zip_urls)} files")
    return downloaded_files


def compute_CATE(data, treatment, outcome, graph):
    try:
        data_clean = data.copy()
        
        if treatment in data_clean.columns:
            data_clean[treatment] = pd.to_numeric(data_clean[treatment], errors='coerce')
        if outcome in data_clean.columns:
            data_clean[outcome] = pd.to_numeric(data_clean[outcome], errors='coerce')
        
        data_clean = data_clean.dropna(subset=[treatment, outcome])
        
        if len(data_clean) < 3:
            return np.nan
        
        model = CausalModel(
            data=data_clean,
            treatment=treatment,
            outcome=outcome,
            graph=graph
        )

        identified_estimand = model.identify_effect()

        estimate = model.estimate_effect(
            identified_estimand,
            method_name='backdoor.linear_regression',
            test_significance=True
        )

        return estimate.value
    except Exception as e:
        print(f"Error in CATE computation for {treatment} -> {outcome}: {e}")
        return np.nan


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


candidate_hyperparameters = ['HW.CPUSingleCore', 'HW.CPUMultiCore', 'HW.GPUScore', 'Model.GPUMemoryPeak', 'HW.MemoryTotal', 'HW.StorageTotal']
encode = []
metrics = {'time_duration': 'Time.Duration'}

zip_urls = [
    "https://causalbench.org/api/runs/profiling/download?profiling_link=runs-602a5a8f-2b37-4350-8f79-410d2683fea7-run.zip",
    "https://causalbench.org/api/runs/profiling/download?profiling_link=runs-d3f722b9-4656-487b-91e4-249474ddfc1e-run.zip",
    "https://causalbench.org/api/runs/profiling/download?profiling_link=runs-3f6c3295-c1bd-4dc2-b4ec-5ca90aa0ae95-run.zip",
    "https://causalbench.org/api/runs/profiling/download?profiling_link=runs-35a8e49b-ed4b-450d-9a31-d8c462b1aae8-run.zip",
    "https://causalbench.org/api/runs/profiling/download?profiling_link=runs-a1d54b10-4e8e-49e4-bf70-da1aa3ae1018-run.zip",
    "https://causalbench.org/api/runs/profiling/download?profiling_link=runs-8c11b472-a624-49fe-a8d0-ad08821d1439-run.zip",
    "https://causalbench.org/api/runs/profiling/download?profiling_link=runs-288c4654-b48b-48d3-940c-c3233274181c-run.zip",
    "https://causalbench.org/api/runs/profiling/download?profiling_link=runs-5fb303ce-b774-49bf-bb5f-b407dfd96ed8-run.zip",
    "https://causalbench.org/api/runs/profiling/download?profiling_link=runs-ff14028d-4e0e-41d9-8027-15ba72beb65b-run.zip",
    "https://causalbench.org/api/runs/profiling/download?profiling_link=runs-3f6c3295-c1bd-4dc2-b4ec-5ca90aa0ae95-run.zip",
    # "https://causalbench.org/api/runs/profiling/download?profiling_link=runs-ef8175d4-65d3-4389-8c29-a79f7bf901ba-run.zip",
    ]


if zip_urls:
    print(f"Fetching {len(zip_urls)} ZIP files from URLs...")
    
    download_dir = tempfile.mkdtemp(prefix="causal_analysis_")
    print(f"Download directory: {download_dir}")
    
    downloaded_files = fetch_zip_files(zip_urls, download_dir)
    
    if downloaded_files:
        try:
            raw_df = process_yaml_data(download_dir, headers)
            print(f"Successfully loaded {len(raw_df)} rows from downloaded files")
        except Exception as e:
            print(f"Error processing downloaded files: {e}")
            print("Falling back to local files...")
    else:
        print("No files downloaded successfully")


hw_cols = [col for col in raw_df.columns if any(hw in col for hw in ['HW.', 'Model.', 'Time.'])]
print(f"Available columns: {hw_cols}")
print(f"Datasets: {raw_df['DS.Name'].unique()}")

hyperparameters = []
for feature in candidate_hyperparameters:
    if feature in raw_df.columns:
        unique_values = raw_df[feature].dropna().unique()
        if len(unique_values) > 1: 
            hyperparameters.append(feature)
            print(f"{feature}: {len(unique_values)} unique values")
        else:
            print(f"{feature}: Only {len(unique_values)} unique value(s) - skipping")
    else:
        print(f"{feature}: Not found in data - skipping")

print(f"Final features to analyze: {hyperparameters}")

df = pd.DataFrame(columns=['dataset'] + hyperparameters + list(metrics.keys()))

for index, row in raw_df.iterrows():
    new_row = []
    
    new_row.append(row['DS.Name']) 

    for hyperparameter in hyperparameters:
        if hyperparameter in row.index and pd.notna(row[hyperparameter]):
            new_row.append(row[hyperparameter])
        else:
            new_row.append(None)
    
    duration_col = metrics['time_duration']  
    if duration_col in row.index and pd.notna(row[duration_col]):
        new_row.append(row[duration_col]/1e9)
    else:
        new_row.append(None)
    
    df.loc[index] = new_row

for index, hyperparameter in enumerate(hyperparameters):
    if index in encode:
        label_encoder = LabelEncoder()
        df[hyperparameter] = label_encoder.fit_transform(df[hyperparameter])
        print(label_encoder.classes_)

print(df)
print()
print()

df = df.dropna()
print(f"After cleaning: {len(df)} experiments remain")

scaler = StandardScaler()

numeric_cols = [col for col in df.columns if col not in ['dataset', 'time_duration']]
print(f"Normalizing columns: {numeric_cols}")

if numeric_cols:
    df_original = df[numeric_cols].copy()
    
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    print("Normalization applied:")
    for col in numeric_cols:
        orig_mean = df_original[col].mean()
        orig_std = df_original[col].std()
        new_mean = df[col].mean()
        new_std = df[col].std()
        print(f"  {col}: mean {orig_mean:.2e} → {new_mean:.3f}, std {orig_std:.2e} → {new_std:.3f}")
else:
    print("No numeric columns found to normalize")

print()

dfs = {key: group for key, group in df.groupby('dataset')}
print(f"Found {len(dfs)} datasets:")
for name, group in dfs.items():
    print(f"  - {name}: {len(group)} experiments")

all_results = {}
total_experiments = 0

for dataset, data in dfs.items():
    print(f'\nProcessing [{dataset}] with {len(data)} experiments...')
    
    if len(data) < 2:
        print("Insufficient data for causal analysis (need at least 2 experiments)")
        continue
        
    try:
        # Single computation - used for both display and saving
        score = compute_score(data)
        
        # Display results
        print("Causal Effects:")
        print(score.to_string(float_format='%.6f'))
        print("\ nLaTeX format:")
        print(score.to_latex(float_format='%.6f'))
        print()
        
        dataset_results = {}
        for hw_feature in score.index:
            effect_value = score.loc[hw_feature, 'time_duration']
            dataset_results[hw_feature] = float(effect_value)
        
        all_results[dataset] = dataset_results
        total_experiments += len(data)
        
    except Exception as e:
        print(f"Error computing causal effects: {e}")
        continue

feature_totals = {}
if all_results:
    for dataset_name, dataset_data in all_results.items():
        for feature, effect in dataset_data.items():
            if feature not in feature_totals:
                feature_totals[feature] = []
            feature_totals[feature].append(effect)
    
    feature_means = {feature: sum(effects)/len(effects) for feature, effects in feature_totals.items()}
    sorted_features = sorted(feature_means.items(), key=lambda x: abs(x[1]), reverse=True)

yaml_results = {
    'causal_effects': {
        'summary': f"Effects on execution time ({len(all_results)} datasets, {total_experiments} experiments)",
        'ranking_by_strength': []
    }
}


yaml_results['causal_effects'] = {}
for dataset_name, dataset_data in all_results.items():
    sorted_dataset_effects = sorted(dataset_data.items(), key=lambda x: abs(x[1]), reverse=True)
    yaml_results['causal_effects'][dataset_name] = {}
    for feature, effect in sorted_dataset_effects:
        yaml_results['causal_effects'][dataset_name][feature] = round(float(effect), 8)

yaml_filename = 'causal_analysis_results.yaml'
with open(yaml_filename, 'w') as yaml_file:
    yaml.dump(yaml_results, yaml_file, default_flow_style=False, indent=2, sort_keys=False)

print(f"Results saved to {yaml_filename}")
print(f"Summary: {len(all_results)} datasets, {total_experiments} experiments, {len(sorted_features)} features")

if sorted_features:
    print(f"\nTop Effects (saved in YAML):")
    for rank, (feature, avg_effect) in enumerate(sorted_features[:3], 1):
        effect_sign = "+" if avg_effect >= 0 else ""
        print(f"  {rank}. {feature}: {effect_sign}{avg_effect:.6f}")

if 'download_dir' in locals() and os.path.exists(download_dir):
    print(f"\n Cleaning up temporary files from {download_dir}")
    import shutil
    try:
        shutil.rmtree(download_dir)
        print("Temporary files cleaned up")
    except Exception as e:
        print(f"Could not clean up temporary files: {e}")

print("\nAnalysis complete!")