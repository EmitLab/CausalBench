import logging
from copy import copy
from zipfile import ZipFile

import yaml
from bunch_py3 import Bunch

from causalbench.formats import SpatioTemporalData, SpatioTemporalGraph
from causalbench.modules.dataset import Dataset
from causalbench.modules.metric import Metric
from causalbench.modules.model import Model
from causalbench.modules.module import Module


class Pipeline(Module):

    def __init__(self, module_id: int = None):
        super().__init__(module_id, 'pipeline')

    def __getstate__(self):
        state = super().__getstate__()
        if 'model' in state and 'object' in state.model:
            del state.model.object
        return state

    def instantiate(self, arguments: Bunch):
        self.type = 'pipeline'
        self.name = arguments.name
        self.task = arguments.task

        # convert dataset to config format
        self.dataset = Bunch()
        if isinstance(arguments.dataset, Dataset):
            self.dataset.object = arguments.dataset
        elif isinstance(arguments.dataset, int):
            self.dataset.id = arguments.dataset

        # convert model to config format
        self.model = Bunch()
        if isinstance(arguments.model[0], Model):
            self.model.id = arguments.model[0].module_id
            self.model.object = arguments.model[0]
        elif isinstance(arguments.model[0], int):
            self.model.id = arguments.model[0]
        self.model.parameters = arguments.model[1]

        # convert metric to config format
        self.metrics = []
        for metric in arguments.metrics:
            self_metric = Bunch()
            if isinstance(metric[0], Metric):
                self_metric.object = metric[0]
            elif isinstance(metric[0], int):
                self_metric.id = metric[0]
            self_metric.parameters = metric[1]
            self.metrics.append(self_metric)

        return f'pipeline/{self.name}.zip'

    def validate(self):
        pass

    def fetch(self, module_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if module_id == 0:
            return 'pipeline/pipeline0.zip'

    def save(self, state) -> bool:
        # TODO: Add database call to upload to the server
        with ZipFile(self.package_path, 'w') as zipped:
            zipped.writestr('config.yaml', yaml.safe_dump(state))
        return True

    def execute(self):
        # load dataset
        if 'object' in self.dataset:
            dataset = self.dataset.object
        elif 'id' in self.dataset:
            dataset = Dataset(self.dataset.id)
        else:
            logging.error(f'Invalid dataset provided: must be an integer or an object of type {Dataset}')
            return

        data = dataset.load()

        # update indices
        if 'files' in self.dataset:
            for file, data_object in data.items():
                if file in self.dataset.files:
                    if isinstance(data_object, SpatioTemporalData):
                        data_object.update_index(self.dataset.files[file])
                    if isinstance(data_object, SpatioTemporalGraph):
                        data_object.update_index(self.dataset.files[file])

        # load model
        if 'object' in self.model:
            model = self.model.object
        elif 'id' in self.model:
            model = Model(self.model.id)
        else:
            logging.error(f'Invalid model provided: must be an integer or an object of type {Model}')
            return

        # map model-data parameters
        parameters = {}
        for model_param, data_param in self.model.parameters.items():
            parameters[model_param] = data[data_param]

        # execute the model
        model_response = model.execute(parameters)

        # metrics
        scores = []
        for self_metric in self.metrics:
            # load the metric
            if 'object' in self_metric:
                metric = self_metric
            elif 'id' in self_metric:
                metric = Metric(self_metric.id)
            else:
                logging.error(f'Invalid metric provided: must be an integer or an object of type {Metric}')
                return

            # check model-metric compatibility
            if model.task != metric.task:
                logging.error(f'The model "{model.name}" and metric "{metric.name}" are not compatible')
                return

            # map metric-data parameters
            parameters = Bunch()
            for metric_param, data_param in self_metric.parameters.items():
                parameters[metric_param] = data[data_param]

            # map metric-model parameters
            if self.task == 'discovery.static':
                parameters.prediction = model_response.output.prediction

            # execute the metric
            metric_response = metric.evaluate(parameters)
            metric_response.id = metric.module_id
            metric_response.name = metric.name
            scores.append(metric_response)

        # form the response
        response = Bunch()

        response.pipeline = Bunch()
        response.pipeline.id = self.module_id
        response.pipeline.name = self.name

        response.dataset = Bunch()
        response.dataset.id = dataset.module_id
        response.dataset.name = dataset.name

        response.model = model_response
        response.model.id = model.module_id
        response.model.name = model.name

        response.metrics = scores

        return response
