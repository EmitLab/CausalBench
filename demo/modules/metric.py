from bunch_py3 import Bunch

from modules.module import Module


class Metric(Module):

    def __init__(self, module_id: int = None):
        super().__init__(module_id, 'metric')

    def instantiate(self, args: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def fetch(self, module_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if module_id == 0:
            return 'metric/shd'

    def evaluate(self, ground, pred):
        # TODO: Execute the metric, change input parameters if necessary
        pass
