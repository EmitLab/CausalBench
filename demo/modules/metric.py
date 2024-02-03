import logging
import os

from bunch_py3 import Bunch, bunchify

from commons.utils import parse_arguments, execute_and_report
from modules.module import Module

class Metric(Module):

    def __init__(self, module_id: int = None):
        super().__init__(module_id, 'metric')

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def validate(self):
        # TODO: Perform logical validation of the structure
        pass

    def fetch(self, module_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if module_id == 0:
            return 'metric/shd.zip'

    def evaluate(self, *args, **keywords):
        # parse the arguments
        arguments: Bunch = parse_arguments(args, keywords)

        # form the proper file path
        file_path = os.path.join(self.base_dir, self.path)

        # map the metric arguments
        metric_args = {}

        if self.task == 'discovery':
            metric_args[self.inputs.ground.id] = arguments.ground_truth
            metric_args[self.inputs.prediction.id] = arguments.prediction

        # execute the metric
        result = execute_and_report(file_path, "evaluate", **metric_args)

        # map the outputs
        output = {}
        for key, data in self.outputs.items():
            output[key] = result[data.id]

        logging.info('Executed metric successfully')

        return bunchify(output)
