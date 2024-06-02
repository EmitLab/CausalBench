import logging
import os

import pandas as pd
from bunch_py3 import Bunch

from causalbench.commons.utils import package_module
from causalbench.formats import SpatioTemporalData, SpatioTemporalGraph
from causalbench.helpers.discovery import adjmat_to_graph
from causalbench.modules.module import Module
from causalbench.services.requests import save_module, fetch_module


class Dataset(Module):

    def __init__(self, module_id: int = None, zip_file: str = None):
        super().__init__(module_id, zip_file, 'dataset')

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def validate(self):
        # TODO: Perform logical validation of the structure
        pass

    def fetch(self, module_id: str):
        return fetch_module('Dataset',
                            module_id,
                            'dataset_version',
                            'downloaded_dataset.zip')

    def save(self, state) -> bool:
        zip_file = package_module(state, self.package_path)
        self.module_id = save_module('Dataset',
                                     zip_file,
                                     'dataset_version',
                                     'dataset.zip')
        return self.module_id is not None

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
