import logging

import pandas as pd
from bunch_py3 import bunchify

from modules.module import Module


class Dataset(Module):

    def __init__(self, dataset_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if dataset_id == 0:
            config_path = 'data/config.yaml'
        else:
            config_path = None

        # set the structure of the current instance
        super().__init__('schema/dataset.json', config_path)

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
