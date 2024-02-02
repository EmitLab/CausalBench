import os

from setuptools import logging

from commons.utils import parse_arguments, execute_and_report
from modules.module import Module
from bunch_py3 import bunchify, Bunch

class Model(Module):

    def __init__(self, model_id: int = None):
        super().__init__(model_id, 'model')

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def fetch(self, model_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if model_id == 0:
            return 'model/pc'

    def execute(self, *args, **keywords): ##TODO: POPULATE
        arguments: Bunch = parse_arguments(args, keywords)
        result = None
        if self.task == 'discovery':
            data = arguments.data
            space = arguments.space
            result = execute_and_report(os.path.join(self.base_dir, self.path), "execute", data=data, space=space)

        #logging.info('Executed data successfully')

        # TODO: Execute the metric, change input parameters if necessary
        return bunchify(result)

    '''
    file_dict = {}

    for file, data in self.files.items():
        file_path = os.path.join(self.base_dir, data.path)

        if data.data == 'dataframe':
            file_df = pd.read_csv(file_path)
        elif data.data == 'graph':
            file_df = pd.read_csv(file_path, index_col=0)

        file_dict[file] = file_df

    logging.info('Loaded dataset successfully')

    return bunchify(file_dict)
'''