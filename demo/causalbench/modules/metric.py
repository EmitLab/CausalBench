import logging
import os

from bunch_py3 import Bunch

from causalbench.commons import executor
from causalbench.commons.utils import package_module
from causalbench.modules.module import Module
from causalbench.services.requests import fetch_module, save_module


class Metric(Module):

    def __init__(self, module_id: int = None, version: int = None, zip_file: str = None):
        super().__init__(module_id, version, zip_file)

    def validate(self):
        # check if the file exists
        file_path = os.path.join(self.package_path, self.path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{self.path}' does not exist in package path '{self.package_path}'")

    def fetch(self):
        return fetch_module(self.schema_name,
                            self.module_id,
                            self.version,
                            'metric_version',
                            'downloaded_metric.zip')

    def save(self, state: dict, public: bool = False) -> bool:
        zip_file = package_module(state, self.package_path)
        self.module_id = save_module(self.schema_name,
                                     self.module_id,
                                     self.version,
                                     public,
                                     zip_file,
                                     'metric_version',
                                     'metric.zip')
        return self.module_id is not None

    def evaluate(self, parameters: Bunch) -> Bunch:
        # form the proper file path
        file_path = os.path.join(self.package_path, self.path)

        # execute the metric
        response: Bunch = executor.execute(file_path, 'evaluate', **parameters)

        logging.info('Executed metric successfully')

        return response
