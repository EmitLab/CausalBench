import logging
import os

from bunch_py3 import Bunch

from commons import executor
from commons.utils import parse_arguments
from modules.module import Module


class Metric(Module):

    def __init__(self, module_id: int = None):
        super().__init__(module_id, 'metric')

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def validate(self):
        # check if the file exists
        if not os.path.exists(os.path.join(self.package_path, self.path)):
            raise FileNotFoundError(f"File '{file_path}' does not exist")

        # check input and output arguments
        if self.task == 'discovery':
            if getattr(self.inputs, "ground", None) is not None:
                raise ValueError('Ground input is missing')
            if getattr(self.inputs, "prediction", None) is not None:
                raise ValueError('Prediction input is missing')
            if getattr(self.outputs, "score", None) is not None:
                raise ValueError('Score output is missing')

    def fetch(self, module_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if module_id == 0:
            return 'metric/shd.zip'
        elif module_id == 1:
            return 'metric/accuracy.zip'
        elif module_id == 2:
            return 'metric/f1.zip'
        elif module_id == 3:
            return 'metric/precision.zip'
        elif module_id == 4:
            return 'metric/recall.zip'

    def save(self, state) -> bool:
        # TODO: Add database call to upload to the server
        pass

    def evaluate(self, *args, **keywords):
        # parse the arguments
        arguments: Bunch = parse_arguments(args, keywords)

        # form the proper file path
        file_path = os.path.join(self.package_path, self.path)

        # map the metric arguments
        metric_args = {}

        if self.task == 'discovery':
            metric_args[self.inputs.ground.id] = arguments.ground_truth
            metric_args[self.inputs.prediction.id] = arguments.prediction

        # execute the metric
        response = executor.execute(file_path, 'evaluate', **metric_args)

        # map the outputs
        output = Bunch()
        for key, data in self.outputs.items():
            output[key] = response.output[data.id]
        response.output = output

        logging.info('Executed metric successfully')

        return response
