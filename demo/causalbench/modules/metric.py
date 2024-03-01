import logging
import os

from bunch_py3 import Bunch

from causalbench.commons import executor
from causalbench.commons.utils import parse_arguments
from causalbench.helpers.discovery import graph_to_adjmat
from causalbench.modules.module import Module


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
            elif getattr(self.inputs.ground, "data") != "graph":
                raise ValueError('Ground input must be a graph for a discovery task')
            if getattr(self.inputs, "prediction", None) is None:
                raise ValueError('Prediction input is missing')
            if getattr(self.inputs.prediction, "data", None) is None:
                raise ValueError('Prediction data is missing')
            elif getattr(self.inputs.prediction, "data") != "graph":
                raise ValueError('Prediction input must be a graph for a discovery task')

            if getattr(self.outputs, "score", None) is None:
                raise ValueError('Score output is missing')

    def fetch(self, module_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if module_id == 0:
            return 'metric/shd_static.zip'
        elif module_id == 1:
            return 'metric/accuracy_static.zip'
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

        if self.task == 'discovery.static':
            metric_args[self.inputs.ground.id] = graph_to_adjmat(arguments.ground_truth)
            metric_args[self.inputs.prediction.id] = graph_to_adjmat(arguments.prediction)
            # self.check_graph(arguments.ground_truth.data)
            # self.check_graph(arguments.prediction.data)

        # execute the metric
        response = executor.execute(file_path, 'evaluate', **metric_args)

        # map the outputs
        output = Bunch()
        for key, data in self.outputs.items():
            output[key] = response.output[data.id]
        response.output = output

        logging.info('Executed metric successfully')

        return response

    # def check_graph(self, data):
    #     if not isinstance(data):
    #         raise TypeError("data must be either numpy.ndarray or pandas.DataFrame")
    #     if data.shape[0] != data.shape[1]:
    #         raise ValueError('data must be in square shape')
