'''
CausalBench Utils:
Publish_all.py
This method publishes all available .zip files in a specified folder path as PUBLIC.
-kpkc
'''

import sys
import os
from unittest.mock import patch
from causalbench.modules.dataset import Dataset
from causalbench.modules.model import Model
from causalbench.modules.metric import Metric
from causalbench.modules.context import Context

# # Specify the folder containing the zip files
folder_path = '../tests/'

# Function that mocks input and always returns 'Y'
def mock_input(prompt):
    if 'y' in prompt.lower() or 'n' in prompt.lower():
        return 'y'  # Automatically answer "Y" to yes/no prompts
    return 'y'  # Default response in other cases

response = input("=== Know that using this method will override further prompts, "
                 "and will publish everything unless stopped. Do you want to continue? (y/n): ===").strip().lower()

if response == 'y':
    print("Continuing...")
else:
    print("Exiting")
    sys.exit()

# Loop through all the files in the folder
datasetpath = folder_path + "data/"#
for file_name in os.listdir(datasetpath):
    if file_name.endswith('.zip'):  # Check if the file is a zip file
        zip_file_path = os.path.join(folder_path, file_name)
        datasetx = Dataset(zip_file=zip_file_path)
        with patch('builtins.input', mock_input):
            datasetx.publish(public=True)
        print(f"Created dataset for: {file_name}")

modelpath = folder_path + "model/"
for file_name in os.listdir(modelpath):
    if file_name.endswith('.zip'):  # Check if the file is a zip file
        zip_file_path = os.path.join(modelpath, file_name)
        print(zip_file_path)
        modelx = Model(zip_file=zip_file_path)
        with patch('builtins.input', mock_input):
            modelx.publish(public=True)

        print(f"Created model for: {file_name}")

metricpath = folder_path + "metric/"
for file_name in os.listdir(metricpath):
    if file_name.endswith('.zip'):  # Check if the file is a zip file
        zip_file_path = os.path.join(metricpath, file_name)
        metricx = Metric(zip_file=zip_file_path)
        with patch('builtins.input', mock_input):
            metricx.publish(public=True)

        print(f"Created metric for: {file_name}")