'''
datasetReader.py: Reads and prepares the dataset wrt config.yaml file.
input: a zip file containing config.yml and dataset (csv format, for now) file.
output: dataframe (representation of the data), s (spatial, if any)
-Kpkc
'''

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

#Define YAML path, check existence
config_file_path = 'data/config.yaml'
check_file_existence(config_file_path, 'YAML config')

#Yaml config and syntax check
config_data = check_yaml_syntax(config_file_path) #Returns none if invalid.

if config_data:
    for file_info in config_data.get('files', []):
        file_path = file_info.get('path', '')
        file_type = file_info.get('type', '')
        dataset_name = config_data.get('name')
        file_info[dataset_name]['path'] # TODO: check this.
        if file_path and file_type:
            dataset_avail = check_file_existence(file_path, file_type)
            if dataset_avail:
                dataset_file_path = file_path + file_type # Will require adjustment for multiple datasets