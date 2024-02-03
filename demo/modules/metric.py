from bunch_py3 import Bunch

from commons.utils import parse_arguments, execute_and_report
from modules.module import Module

import os
class Metric(Module):

    def __init__(self, module_id: int = None):
        super().__init__(module_id, 'metric')

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def fetch(self, module_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if module_id == 0:
            return 'metric/shd'

    def evaluate(self, *args, **keywords):
        arguments: Bunch = parse_arguments(args, keywords)

        if self.task == 'discovery':
            ground_truth = arguments.ground_truth
            prediction = arguments.prediction
            mpath = os.path.join(self.base_dir, self.path)
            result = execute_and_report(mpath, self.name, pred=prediction, truth=ground_truth)
            return result
