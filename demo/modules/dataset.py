import logging
import os

import pandas as pd
from bunch_py3 import Bunch

from modules.module import Module


class Dataset(Module):

    def __init__(self, module_id: int = None):
        super().__init__(module_id, 'dataset')

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def validate(self):
        # TODO: Perform logical validation of the structure
        pass

    def fetch(self, module_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if module_id == 0:
            return 'data/abalone.zip'

    def save(self, state) -> bool:
        # TODO: Add database call to upload to the server
        pass

    def load(self):
        files = Bunch()

        for file, data in self.files.items():
            # form the proper file path
            file_path = os.path.join(self.package_path, data.path)

            # read the file
            if data.data == 'dataframe':
                file_df = pd.read_csv(file_path)
            elif data.data == 'graph':
                file_df = pd.read_csv(file_path, index_col=0)

            # add the loaded file to the dictionary
            files[file] = file_df

            for column, col_data in data.columns.items():
                if data.headers == True:
                    col_df = file_df[col_data.header]
                else:
                    col_df = file_df[col_data.index]
                
                if col_data.data == 'integer':
                    if not pd.api.types.is_integer_dtype(col_df):
                        raise TypeError(f'Data type mismatch for column {column}')
                    if 'labels' in col_data:
                        labels = sorted(col_data.labels)
                        data_labels = sorted(file_df[col_data.header].unique())
                        if(labels!=data_labels):
                            raise ValueError(f'Labels do not match for column {column}')
                    if 'range' in col_data:
                        start = col_data.range.start
                        end = col_data.range.end
                        min1 = min(file_df[col_data.header])
                        max1 = max(file_df[col_data.header])
                        if not (min1>=start and min1<=end and max1>=start and max1<=end):
                            raise ValueError(f'Range does not match for column {column}')
                elif col_data.data =='decimal':
                    if not pd.api.types.is_float_dtype(col_df):
                        raise TypeError(f'Data type mismatch for column {column}')
                    if 'labels' in col_data:
                        labels = sorted(col_data.labels)
                        data_labels = sorted(file_df[col_data.header].unique())
                        if labels!=data_labels:
                            raise ValueError(f'Labels do not match for column {column}')
                    if 'range' in col_data:
                        start = col_data.range.start
                        end = col_data.range.end
                        min1 = min(file_df[col_data.header])
                        max1 = max(file_df[col_data.header])
                        if not (min1>=start and min1<=end and max1>=start and max1<=end):
                            raise ValueError(f'Range does not match for column {column}')
                        
        logging.info('Loaded dataset successfully')

        return files
