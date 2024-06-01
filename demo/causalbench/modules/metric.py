import logging
import os

from bunch_py3 import Bunch

from causalbench.commons import executor
from causalbench.commons.utils import parse_arguments, package_module
from causalbench.modules.module import Module
from causalbench.services.requests import fetch_module, save_module


class Metric(Module):

    def __init__(self, module_id: int = None, zip_file: str = None):
        super().__init__(module_id, zip_file, 'metric')

    def validate(self):
        # check if the file exists
        file_path = os.path.join(self.package_path, self.path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{self.path}' does not exist in package path '{self.package_path}'")

        # check input and output arguments
        if self.task == 'discovery':
            if getattr(self.inputs, "ground", None) is None:
                raise ValueError('Ground input is missing')
            if getattr(self.inputs.ground, "data", None) is None:
                raise ValueError('Ground data is missing')
            elif getattr(self.inputs.ground, "data") not in ["graph.static", "graph.temporal"]:
                raise ValueError('Ground input must be a graph for a discovery task')
            if getattr(self.inputs, "prediction", None) is None:
                raise ValueError('Prediction input is missing')
            if getattr(self.inputs.prediction, "data", None) is None:
                raise ValueError('Prediction data is missing')
            elif getattr(self.inputs.prediction, "data") not in ["graph.static", "graph.temporal"]:
                raise ValueError('Prediction input must be a graph for a discovery task')

            if getattr(self.outputs, "score", None) is None:
                raise ValueError('Score output is missing')

    def fetch(self, module_id: int):
        return fetch_module(module_id, 'metric_version', 'downloaded_metric.zip')

    def save(self, state) -> bool:
        zip_file = package_module(state, self.package_path)
        return save_module(zip_file, 'metric_version', 'metric.zip')

    def evaluate(self, *args, **keywords):
        # parse the arguments
        arguments: Bunch = parse_arguments(args, keywords)

        # form the proper file path
        file_path = os.path.join(self.package_path, self.path)

        # map the metric arguments
        metric_args = {}

        if self.task in ['discovery.static', 'discovery.temporal', 'classification']:
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
