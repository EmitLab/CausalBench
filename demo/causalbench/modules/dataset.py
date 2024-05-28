import logging
import os
import requests

import pandas as pd
from bunch_py3 import Bunch

from causalbench.formats import SpatioTemporalData, SpatioTemporalGraph
from causalbench.helpers.discovery import adjmat_to_graph
from causalbench.modules.module import Module


class Dataset(Module):

    def __init__(self, module_id: int = None):
        super().__init__(module_id, 'dataset')

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def validate(self):
        # TODO: Perform logical validation of the structure
        pass

    def fetch(self, module_id: str):
        # TODO: Replace with database call to download zip and obtain path
        filename = None
        print(f"MODULE: {module_id}")
        url = f'http://127.0.0.1:8000/dataset_version/download/{module_id}/'
        headers = {
            'User-Agent': 'insomnia/2023.5.8'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Extract filename from the Content-Disposition header if available
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                filename = content_disposition.split('filename=')[-1].strip('"')
            else:
                # Fallback to a default name if the header is not present
                filename = 'downloaded_dataset.zip'
            
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f'Download successful, saved as {filename}')
        else:
            print(f'Failed to download file: {response.status_code}')
            print(response.text)
        return filename
        if module_id == 0:
            return 'data/abalone.zip'
        elif module_id == 1:
            return 'data/adult.zip'
        elif module_id == 2:
            return 'data/time_series_simulated.zip'
        elif module_id == 3:
            return 'data/fashion_mnist.zip'

    def save(self, state) -> bool:
        # TODO: Add database call to upload to the server
        input_file_path = input("Enter the path of dataset.zip file: ")
        input_file_path = "/home/abhinavgorantla/emitlab/causal_bench/CausalBench/zipfiles/dataset.zip"
        print(f"Saving dataset!")

        url = 'http://127.0.0.1:8000/dataset_version/upload/'
        headers = {
            # 'Content-Type': 'application/json'
        }
        files = {
            'file': ('dataset.zip', open(input_file_path, 'rb'), 'application/zip')
        }

        response = requests.post(url, headers=headers, files=files)
        print(response.status_code)
        print(response.text)

    def load(self) -> Bunch:
        files = Bunch()

        for file, data in self.files.items():
            # form the proper file path
            file_path = str(os.path.join(self.package_path, data.path))

            # read the file
            file_df = None
            data_object = None
            if data.data == 'dataframe':
                file_df = pd.read_csv(file_path)
                data_object = SpatioTemporalData(file_df)
                data_object.update_index(data)

            elif data.data == 'graph.static':
                file_df = pd.read_csv(file_path, index_col=0)
                data_object = adjmat_to_graph(file_df.to_numpy(), file_df.columns)

            elif data.data == 'graph.temporal':
                file_df = pd.read_csv(file_path)
                data_object = SpatioTemporalGraph(file_df)
                data_object.update_index(data)

            if file_df is None:
                raise ValueError(f'Invalid data type {data.data}')

            # add data object to the dictionary
            files[file] = data_object

            # validate the file structure
            for column, col_data in data.columns.items():
                if data.headers:
                    col_df = file_df[col_data.header]
                else:
                    col_df = file_df[col_data._index]

                if col_data.data == 'integer':
                    if not pd.api.types.is_integer_dtype(col_df):
                        raise TypeError(f'Data type mismatch for column {column}')
                    if 'labels' in col_data:
                        labels = sorted(col_data.labels)
                        data_labels = sorted(file_df[col_data.header].unique())
                        if labels != data_labels:
                            raise ValueError(f'Labels do not match for column {column}')
                    if 'range' in col_data:
                        start = col_data.range.start
                        end = col_data.range.end
                        min1 = min(file_df[col_data.header])
                        max1 = max(file_df[col_data.header])
                        if not (start <= min1 <= end and start <= max1 <= end):
                            raise ValueError(f'Range does not match for column {column}')

                elif col_data.data == 'decimal':
                    if not pd.api.types.is_float_dtype(col_df):
                        raise TypeError(f'Data type mismatch for column {column}')
                    if 'labels' in col_data:
                        labels = sorted(col_data.labels)
                        data_labels = sorted(file_df[col_data.header].unique())
                        if labels != data_labels:
                            raise ValueError(f'Labels do not match for column {column}')
                    if 'range' in col_data:
                        start = col_data.range.start
                        end = col_data.range.end
                        min1 = min(file_df[col_data.header])
                        max1 = max(file_df[col_data.header])
                        if not (start <= min1 <= end and start <= max1 <= end):
                            raise ValueError(f'Range does not match for column {column}')

        logging.info('Loaded dataset successfully')

        return files
