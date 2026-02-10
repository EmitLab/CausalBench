# Adding a Dataset to CausalBench

```mermaid
flowchart LR
    Schema[Define schema] --> Download[Download data]
    Download --> Config[Create config.yaml]
    Config --> Bundle[Bundle zip]
    Bundle --> Test[Test locally]
    Test --> Publish[Push & publish]
```

This guide explains how to add a new dataset to the CausalBench platform.

## Overview

Adding a dataset involves five main steps:
1. Understanding the dataset schema
2. Downloading and preparing the data
3. Creating the configuration file
4. Bundling the dataset
5. Testing and publishing

## 1. Understanding the Dataset Schema

### Required Fields

Every dataset must have a `config.yaml` file with the following required fields:

```yaml
causalbench:            # Version compatibility info
    major: '0'
    minor: '2'
    build: '0'
type: dataset           # Must be 'dataset'
name: my_dataset        # Unique identifier (alphanumeric, underscores, hyphens)
source: UCI             # Data source (e.g., UCI, sklearn, kaggle)
url: https://...        # Original data source URL
description: ...        # Brief description of the dataset
files:                  # Dictionary of files (at least one required)
    file1:              # File identifier
        # File configuration...
```

### File Configuration

Each file in the `files` dictionary must specify:

```yaml
file1:
    type: csv                    # Currently only 'csv' supported
    data: dataframe              # Type: 'dataframe', 'graph.static', or 'graph.temporal'
    path: data.csv               # Relative path to the CSV file
    headers: true                # Whether CSV has header row
    columns:                     # Dictionary of column definitions
        column_name:             # Logical column name (used in code)
            index: 0             # Zero-based column position
            header: ActualName   # Actual column name in CSV (if headers: true)
            data: decimal        # Data type: 'integer', 'decimal', or 'string'
            # Optional fields:
            labels: [0, 1, 2]    # For categorical data (list of valid values)
            range:               # For numerical data
                start: 0.0
                end: 1.0
            unit: meters         # Unit of measurement (optional, not used in validation)
```

### Index Field (Optional)

For datasets with prediction targets or temporal/spatial structure:

```yaml
file1:
    # ... other fields ...
    index:
        target: target_column    # For regression/classification tasks
        time: time_column        # For temporal data
        location: location_col   # For spatial data
        # For causal graphs:
        cause: cause_column
        effect: effect_column
        strength: strength_column
        lag: lag_column
```

The index values reference column names defined in the `columns` section.

### Important Notes About Fields

- **`type` field in columns**: This field is **NOT used** by the validation code. If you want to keep it for metadata, leave it blank (`type:`) or set it to `null` (e.g., `nominal`, `ratio`).
- **`data` field**: This is the **critical field** that determines validation behavior:
  - `integer`: Validates as integer type, supports `labels` and `range`
  - `decimal`: Validates as float type, supports `labels` and `range`
  - `string`: For text data (minimal validation)
- **`index` property**: Required for each column - the zero-based position in the CSV
- **`unit` field**: Optional metadata, not used in validation

### Data Types Explained

**`data` field in files:**
- `dataframe`: Tabular data (most common)
- `graph.static`: Static causal graph (adjacency matrix)
- `graph.temporal`: Temporal causal graph

**`data` field in columns:**
- `integer`: Whole numbers (validated with `pd.api.types.is_integer_dtype`)
- `decimal`: Floating point numbers (validated with `pd.api.types.is_float_dtype`)
- `string`: Text data

## 2. Download and Prepare Data

### Create a Dataset Directory

```bash
cd causalbench-asu/tests/data
mkdir my_dataset
cd my_dataset
```

### Download the Data

Create a `download_data.py` script to fetch and prepare your data:

```python
"""
Download My Dataset from [source]
"""

from sklearn.datasets import load_your_dataset  # Example

def download_data():
    # Load the dataset
    data = load_your_dataset(as_frame=True)

    # Prepare the data (clean, transform, etc.)
    df = data.frame

    # Save to CSV
    df.to_csv("my_dataset_data.csv", index=False)

    print(f"Dataset saved with {len(df)} samples")
    print(f"Features: {list(df.columns)}")

if __name__ == "__main__":
    download_data()
```

Run the script:

```bash
python download_data.py
```

## 3. Create Configuration File

### Example: Regression Dataset

```yaml
# My Dataset: description URL
causalbench:
    major: '0'
    minor: '2'
    build: '0'
type: dataset
name: my_dataset
source: sklearn
url: https://example.com/dataset
description: Predict target variable from features (regression task)
files:
    file1:
        type: csv
        data: dataframe
        path: my_dataset_data.csv
        headers: true
        index:
            target: target_var  # Specify the prediction target
        columns:
            feature1:
                index: 0
                header: feature1
                data: decimal
            feature2:
                index: 1
                header: feature2
                data: integer
                labels: [0, 1, 2]  # Categorical with 3 classes
            target_var:
                index: 2
                header: target_var
                data: decimal
                range:
                    start: 0.0
                    end: 100.0
```

### Example: Classification Dataset

```yaml
files:
    file1:
        type: csv
        data: dataframe
        path: data.csv
        headers: true
        index:
            target: class_label
        columns:
            class_label:
                index: 0
                header: class
                data: integer
                labels: [0, 1]  # Binary classification
```

### Example: With Causal Graph

```yaml
files:
    file1:
        type: csv
        data: dataframe
        path: observations.csv
        headers: true
        columns:
            # ... column definitions ...

    file2:
        type: csv
        data: graph.static
        path: causal_graph.csv
        headers: true
        columns:
            # Adjacency matrix columns (all integer 0/1)
            var1:
                index: 0
                header: var1
                data: integer
            var2:
                index: 1
                header: var2
                data: integer
```

## 4. Bundle the Dataset

Use the `zip_files.py` script to create a zip archive:

### Preview (Dry Run)

```bash
cd causalbench-asu/tests
python zip_files.py "data/my_dataset" --dry-run
```

This shows what will be zipped without creating files.

### Create the Zip

```bash
python zip_files.py "data/my_dataset"
```

This creates `data/my_dataset.zip` containing all files in the dataset directory.

### Bundle Multiple Datasets

```bash
python zip_files.py "data/dataset1,data/dataset2"
```

## 5. Test and Publish

### Test Loading the Dataset

Create a test script:

```python
from causalbench.modules import Dataset

# Load from zip file
dataset = Dataset(zip_file="path/to/my_dataset.zip")

# Load the data
files = dataset.load()

# Access the data
print(files.file1.data.head())

# If you specified a target index
if hasattr(files.file1, 'target'):
    print(f"Target column: {files.file1.target}")
```

### Validation

The schema validation happens automatically when you load a dataset. It checks:

1. **Schema compliance**: All required fields present
2. **Version compatibility**: CausalBench version matches
3. **Data type validation**:
   - Integer columns contain integers
   - Decimal columns contain floats
4. **Label validation**: If `labels` specified, data values match
5. **Range validation**: If `range` specified, all values within bounds

### Publish to CausalBench

```python
from causalbench.modules import Dataset

# Load your dataset
dataset = Dataset(zip_file="data/my_dataset.zip")

# Publish (requires authentication)
dataset.publish(public=True)  # Makes it available to all users
```

## Common Patterns

### Regression Dataset

- Set `index.target` to the prediction column
- Use `data: decimal` for continuous features
- Use `data: integer` for discrete features
- Add `range` for bounded values

### Classification Dataset

- Set `index.target` to the class label column
- Use `data: integer` for class labels
- Specify all classes in `labels`

### Time Series Dataset

- Set `index.time` to the time column
- Set `index.target` for prediction tasks
- Use `data: integer` for timestamps or `data: decimal` for continuous time

### Causal Discovery Dataset

- `file1`: Observational data
- `file2`: Ground truth causal graph (adjacency matrix)
- Use `data: graph.static` for the graph file
