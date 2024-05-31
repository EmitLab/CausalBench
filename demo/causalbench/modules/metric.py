import logging
import os
import requests
from bunch_py3 import Bunch

from causalbench.commons import executor
from causalbench.commons.utils import parse_arguments
from causalbench.modules.module import Module

from causalbench.services.requests import fetch_module, save_module

class Metric(Module):

    def __init__(self, module_id: int = None):
        super().__init__(module_id, 'metric')

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

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
        response = fetch_module(module_id, "metric_version", "downloaded_metric.zip")

        return response
    def save(self, state, access_token) -> bool:
        # TODO: Add database call to upload to the server
        input_file_path = input("Enter the path of metric.zip file: ")
        # input_file_path = "/home/abhinavgorantla/emitlab/causal_bench/CausalBench/demo/tests/metric/f1_static.zip"
        print(f"Saving metric!")
        response = save_module(input_file_path, access_token, "metric_version", "metric.zip")

        return response

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
