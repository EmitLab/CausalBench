import logging
import os

from bunch_py3 import Bunch

from causalbench.commons import executor
from causalbench.commons.utils import package_module
from causalbench.modules.module import Module
from causalbench.services.requests import save_module, fetch_module


class Model(Module):

    def __init__(self, module_id: int = None, version: int = None, zip_file: str = None):
        super().__init__(module_id, version, zip_file)

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def validate(self):
        # TODO: Perform logical validation of the structure
        pass

    def fetch(self):
        return fetch_module(self.schema_name,
                            self.module_id,
                            self.version,
                            'model_version',
                            'downloaded_model.zip')

    def save(self, state: dict, public: bool = False) -> bool:
        zip_file = package_module(state, self.package_path)
        self.module_id = save_module(self.schema_name,
                                     self.module_id,
                                     self.version,
                                     public,
                                     zip_file,
                                     'model_version',
                                     'model.zip')
        return self.module_id is not None

    def execute(self, parameters: Bunch) -> Bunch:
        # form the proper file path
        file_path = os.path.join(self.package_path, self.path)

        # execute the model
        response: Bunch = executor.execute(file_path, 'execute', **parameters)

        logging.info('Executed model successfully')

        return response
