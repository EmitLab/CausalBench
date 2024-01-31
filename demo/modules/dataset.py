import logging

import pandas as pd
from bunch_py3 import bunchify

from modules.module import Module


class Dataset(Module):

    def __init__(self, module_id: int):
        super().__init__(module_id, 'schema/dataset.json')

    def instantiate(self):
        # TODO: Create the structure of the new instance
        pass

    def fetch(self, module_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if module_id == 0:
            return 'data/config.yaml'

    def load(self):
        # load the dataset
        dataset_df = pd.read_csv(self.files.dataset.path)

        # load the ground truth
        ground_truth_df = pd.read_csv(self.files.ground_truth.path, index_col=0)

        logging.info('Loaded dataset successfully')

        # form the response dictionary
        response = {'dataset': dataset_df,
                    'ground_truth': ground_truth_df}

        return bunchify(response)
