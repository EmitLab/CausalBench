import logging
import os
import requests

from bunch_py3 import Bunch

from demo.causalbench.commons import executor
from demo.causalbench.commons.utils import parse_arguments
from demo.causalbench.modules.module import Module
from demo.causalbench.services.requests import save_module, fetch_module

class Model(Module):

    def __init__(self, model_id: int = None):
        super().__init__(model_id, 'model')

    def instantiate(self, arguments: Bunch):
        self.type = 'model'
        self.name = arguments.name
        self.task = arguments.task
        self.path = arguments.path

        self.inputs = Bunch()

        # Populate the inputs and outputs. However, we may have different types of input (data) and output (prediction)
        '''
        if isinstance(arguments.inputs[0], %dataObj%):
            self.model.id = arguments.model[0].module_id
            self.model.object = arguments.model[0]
        '''
        #TODO: Talk with pratanu.

        return f'model/{self.name}.zip'


        # TODO: Create the structure of the new instance
        pass

    def validate(self):

        if 'data' not in self.inputs:
            raise ValueError('Input does not include a \'data\' field')
        if 'id' is None in self.inputs.data:
            raise ValueError('Input id is missing')
        if 'data' is None in self.inputs.data:
            raise ValueError('Input data is missing')

        if self.task == 'discovery.static':
            if 'prediction' not in self.outputs:
                raise ValueError('Output does not include a \'prediction\' field')
            if 'id' is None in self.outputs.prediction:
                raise ValueError('Output id is missing')
            if 'data' is None in self.outputs.prediction:
                raise ValueError('Output data is missing')

        if self.task == 'classification':
            if 'prediction' not in self.outputs:
                raise ValueError('Output does not include a \'prediction\' field')
            if 'id' is None in self.outputs.prediction:
                raise ValueError('Output id is missing')
            if 'data' is None in self.outputs.prediction:
                raise ValueError('Output data is missing')

        if self.task == 'discovery.temporal':
            if 'prediction' not in self.outputs:
                raise ValueError('Output does not include a \'prediction\' field')
            if 'id' is None in self.outputs.prediction:
                raise ValueError('Output id is missing')
            if 'data' is None in self.outputs.prediction:
                raise ValueError('Output data is missing')

            # TODO: Perform logical validation of the structure
        pass

    def fetch(self, model_id: int):
        response = fetch_module(model_id, "model_version", "downloaded_model.zip")

        return response

    def save(self, state, access_token) -> bool:
        # TODO: Add database call to upload to the server
        # input_file_path = input("Enter the path of model.zip file: ")
        input_file_path = "/home/abhinavgorantla/emitlab/causal_bench/CausalBench/zipfiles/model.zip"
        print(f"Saving model!")
        response = save_module(input_file_path, access_token, "model_version", "model.zip")

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
