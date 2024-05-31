import logging
import os

from bunch_py3 import Bunch

from causalbench.commons import executor
from causalbench.commons.utils import parse_arguments
from causalbench.modules.module import Module


class Model(Module):

    def __init__(self, model_id: int = None):
        super().__init__(model_id, 'model')

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
        # TODO: Replace with database call to download zip and obtain path
        if model_id == 0:
            return 'model/pc.zip'
        elif model_id == 1:
            return 'model/ges.zip'
        elif model_id == 2:
            return 'model/lingam.zip'
        elif model_id == 3:
            return 'model/ermirmcfcminst.zip'

    def save(self, state) -> bool:
        # TODO: Add database call to upload to the server
        pass

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
