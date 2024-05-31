import logging
import os
import requests

from bunch_py3 import Bunch

from causalbench.commons import executor
from causalbench.commons.utils import parse_arguments
from causalbench.modules.module import Module
from causalbench.services.requests import save_module, fetch_module

class Model(Module):

    def __init__(self, model_id: int = None, zip_file: str = None):
        super().__init__(model_id, zip_file, 'model')

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def validate(self):
        if self.task == 'discovery.static':
            if 'data' not in self.inputs:
                raise ValueError('Input does not include a \'data\' field')
            if 'prediction' not in self.outputs:
                raise ValueError('Output does not include a \'prediction\' field')

            # TODO: Perform logical validation of the structure
        pass

    def fetch(self, model_id: int):
        return fetch_module(model_id, "model_version", "downloaded_model.zip")

    def save(self, state) -> bool:
        # TODO: Add database call to upload to the server
        input_file_path = input("Enter the path of model.zip file: ")
        # input_file_path = "/home/abhinavgorantla/emitlab/causal_bench/CausalBench/demo/tests/model/pc.zip"
        print(f"Saving model!")
        response = save_module(input_file_path, "model_version", "model.zip")

        return response

    def execute(self, *args, **keywords):
        # parse the arguments
        arguments: Bunch = parse_arguments(args, keywords)

        # form the proper file path
        file_path = os.path.join(self.package_path, self.path)

        # map the model arguments
        model_args = {}
        print(self.task)
        if self.task == 'discovery.static':
            model_args[self.inputs.data.id] = arguments.data

        elif self.task == 'discovery.temporal':
            model_args[self.inputs.data.id] = arguments.data

        elif self.task == 'discovery.spatiotemporal':
            model_args[self.inputs.data.id] = arguments.data
            model_args[self.inputs.space.id] = arguments.space if 'space' in arguments else None

        elif self.task == 'classification':
            model_args[self.inputs.data.id] = arguments.data
            model_args[self.inputs.target.id] = arguments.target
        else:
            raise TypeError(f'Invalid task type: {self.task}')

        # execute the model
        response = executor.execute(file_path, 'execute', **model_args)

        # map the outputs
        output = Bunch()
        for key, data in self.outputs.items():
            output[key] = response.output[data.id]
        response.output = output

        logging.info('Executed model successfully')

        return response
