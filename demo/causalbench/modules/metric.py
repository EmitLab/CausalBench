import logging
import os

from bunch_py3 import Bunch

from causalbench.commons import executor
from causalbench.commons.utils import parse_arguments
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
        # TODO: Replace with database call to download zip and obtain path
        if module_id == 0:
            return 'metric/shd_static.zip'
        elif module_id == 1:
            return 'metric/accuracy_static.zip'
        elif module_id == 2:
            return 'metric/f1_static.zip'
        elif module_id == 3:
            return 'metric/precision_static.zip'
        elif module_id == 4:
            return 'metric/recall_static.zip'
        elif module_id == 5:
            return 'metric/shd_temporal.zip'
        elif module_id == 6:
            return 'metric/accuracy_temporal.zip'
        elif module_id == 7:
            return 'metric/f1_temporal.zip'
        elif module_id == 8:
            return 'metric/precision_temporal.zip'
        elif module_id == 9:
            return 'metric/recall_temporal.zip'
        else:
            raise ValueError(f"Invalid module_id: {module_id}")

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

        if self.task == 'discovery.static' or self.task == 'discovery.temporal':
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
