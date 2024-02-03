import logging
import os

from bunch_py3 import bunchify, Bunch

from commons.utils import parse_arguments, execute_and_report
from modules.module import Module


class Model(Module):

    def __init__(self, model_id: int = None):
        super().__init__(model_id, 'model')

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def validate(self):
        # TODO: Perform logical validation of the structure
        pass

    def fetch(self, model_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if model_id == 0:
            return 'model/pc.zip'

    def execute(self, *args, **keywords):
        # parse the arguments
        arguments: Bunch = parse_arguments(args, keywords)

        # form the proper file path
        file_path = os.path.join(self.base_dir, self.path)

        # map the model arguments
        model_args = {}

        if self.task == 'discovery':
            model_args[self.inputs.data.id] = arguments.data
            model_args[self.inputs.space.id] = arguments.space if 'space' in arguments else None

        # execute the model
        result = execute_and_report(file_path, "execute", **model_args)

        # map the outputs
        output = {}
        for key, data in self.outputs.items():
            output[key] = result[data.id]

        logging.info('Executed model successfully')

        return bunchify(output)
