import logging

import pandas as pd
from bunch_py3 import bunchify

from modules.module import Module


class Dataset(Module):

    def __init__(self, module_id: int = None):
        super().__init__(module_id, 'schema/dataset.json')

    def instantiate(self):
        # TODO: Create the structure of the new instance
        pass

    def fetch(self, module_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if module_id == 0:
            return 'data/abalone/config.yaml'

    def load(self):
        file_dict = {}

        for file, data in self.files.items():
            if data.data == 'dataframe':
                file_df = pd.read_csv(data.path)
            elif data.data == 'graph':
                file_df = pd.read_csv(data.path, index_col=0)

            file_dict[file] = file_df

        logging.info('Loaded dataset successfully')

        return bunchify(file_dict)
