'''
datasetReader.py: Reads and prepares the dataset wrt config.yaml file.
input: a zip file containing config.yml and dataset (csv format, for now) file.
output: dataframe (representation of the data), s (spatial, if any)
-Kpkc
'''
#DataDEF: Causal info order-  Sex	Length	Diam	Height	Whole	Shucked	Viscera	Shell	Rings

#imports
import pandas as pd
import os
import yaml

# Check the zip
    #(impl later as part of task)

# Check if the data file and config exists
def check_file_existence(file_path, file_type):
    if os.path.exists(file_path):
        print(f"{file_type} file '{file_path}' exists.")
        return True
    else:
        print(f"Error: {file_type} file '{file_path}' not found!")
        return False
def check_yaml_syntax(yaml_path):
    try:
        with open(yaml_path, 'r') as yaml_file:
            config_data = yaml.safe_load(yaml_file)
        print(f"YAML syntax in '{yaml_path}' is valid.")
        return config_data
    except Exception as e:
        print(f"Error: Invalid YAML syntax in '{yaml_path}': {e}")
        return None

#def read_dataset():
#Define YAML path, check existence
config_file_path = 'data/config.yaml'
check_file_existence(config_file_path, 'YAML config')

#Yaml config and syntax check
config_data = check_yaml_syntax(config_file_path) #Returns none if invalid.

first_checked = False

#There should be an indicator what the file is, as in dataset parts or ground truths, as they will get processed separately.
#However, We expect to see two files in the demo case, it is done with such an assumption and will be updated after oncoming meetings.
dataframes = []

if config_data:
    dataset_name = config_data.get('name', '')
    file_paths = []


    for file_info in config_data.get('files', []):
        dataset_file =  file_info.get('dataset')
        groundtruth_file = file_info.get('groundtruth')

        if dataset_file:
        #this statement won't run if the file is groundtruth:
            dataset_file_path = dataset_file.get('path','')
        # Check existence
            if check_file_existence(dataset_file_path, '.csv'):
                df_data = pd.read_csv(dataset_file_path)
                dataframes.append(df_data)
                print("Dataset is set.")

        if groundtruth_file:
        #this statement won't run if the file is dataset:
            groundtruth_file_path = groundtruth_file.get('path', '')
        # Check existence
            if check_file_existence(groundtruth_file_path, '.csv'):
                df_groundtruth = pd.read_csv(groundtruth_file_path, header=0,index_col=0)
                dataframes.append(df_groundtruth)
                print("Groundtruth is set.")

        #Q: how do we check for causal info? should we always expect a ground truth?
        #TODO: Add both files into an array then parse-send them as such.

# Print the dataset characteristics.
print (dataframes)
    #return dataframes