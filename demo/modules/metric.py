from bunch_py3 import Bunch

from commons.utils import parse_arguments
from modules.module import Module


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
            ground_truth = self.ground
            prediction = self.prediction

            return SHD(prediction, ground_truth)
