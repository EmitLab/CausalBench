import logging

import pandas as pd
from bunch_py3 import bunchify

from commons.utils import execute_and_report
from modules.module import Module


class Dataset(Module):

    def __init__(self, module_id: int = None):
        super().__init__(module_id, 'schema/metric.json')

    def instantiate(self):
        # TODO: Create the structure of the new instance
        pass

    def fetch(self, module_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if module_id == 0:
            return 'metric/shd'

    def execute(self, ground, pred):
        # TODO: Execute the metric, change input parameters if necessary
        pass
