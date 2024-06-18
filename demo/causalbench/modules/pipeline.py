import logging
from datetime import datetime

from bunch_py3 import Bunch

from causalbench.commons.utils import parse_arguments, package_module, causal_bench_path
from causalbench.formats import SpatioTemporalData, SpatioTemporalGraph
from causalbench.modules.dataset import Dataset
from causalbench.modules.metric import Metric
from causalbench.modules.model import Model
from causalbench.modules.module import Module
from causalbench.modules.run import Run
from causalbench.services.requests import save_module, fetch_module


class Pipeline(Module):

    def __init__(self, module_id: int = None, version: int = None, zip_file: str = None):
        super().__init__(module_id, version, zip_file, 'pipeline')

    def __getstate__(self):
        state = super().__getstate__()

        if 'dataset' in state and 'object' in state.dataset:
            del state.dataset.object

        if 'model' in state and 'object' in state.model:
            del state.model.object

        if 'metrics' in state:
            for metric in state.metrics:
                if 'object' in metric:
                    del metric.object

        return state

    def validate(self):
        # TODO: To be implemented
        pass

    def fetch(self):
        return fetch_module('Pipeline',
                            self.module_id,
                            self.version,
                            'pipelines',
                            'downloaded_pipeline.zip')

    def save(self, state) -> bool:
        if state.dataset.id is None:
            logging.error(f'Cannot publish pipeline as it contains unpublished dataset')
            return False

        if state.model.id is None:
            logging.error('Cannot publish pipeline as it contains unpublished model')
            return False

        for metric in state.metrics:
            if metric.id is None:
                logging.error('Cannot publish pipeline as it contains unpublished metric')
                return False

        zip_file = package_module(state, self.package_path)
        self.module_id = save_module('Pipeline',
                                     self.module_id,
                                     zip_file,
                                     'pipelines',
                                     'pipeline.zip')
        return self.module_id is not None

    def execute(self) -> Run | None:
        # execution start time
        start_time = datetime.now()

        # load data
        data = self.dataset.object.load()

        # # update indices
        # if 'files' in self.dataset:
        #     for file, data_object in data.items():
        #         if file in self.dataset.files:
        #             if isinstance(data_object, SpatioTemporalData):
        #                 data_object.update_index(self.dataset.files[file])
        #             if isinstance(data_object, SpatioTemporalGraph):
        #                 data_object.update_index(self.dataset.files[file])

        # map model-data parameters
        parameters = {}
        for model_param, data_param in self.model.parameters.items():
            parameters[model_param] = data[data_param]

        # execute the model
        model_response: Bunch = self.model.object.execute(parameters)

        # metrics
        scores = []
        for self_metric in self.metrics:
            # check model-metric compatibility
            if self.model.object.task != self_metric.object.task:
                logging.error(f'The model "{self.model.object.name}" and metric "{self_metric.object.name}" are not compatible')
                return
            logging.info("Checked model-metric compatibility")

            # map metric-data parameters
            parameters = Bunch()
            for metric_param, data_param in self_metric.parameters.items():
                parameters[metric_param] = data[data_param]

            # map metric-model parameters
            if self.task in ['discovery.static', 'discovery.temporal', 'classification']:
                parameters.prediction = model_response.output.prediction

            # execute the metric
            metric_response = self_metric.object.evaluate(parameters)
            metric_response.id = self_metric.object.module_id
            metric_response.name = self_metric.object.name
            scores.append(metric_response)

        # execution end time
        end_time = datetime.now()

        # form the response
        run = Run()

        run.pipeline = Bunch()
        run.pipeline.id = self.module_id
        run.pipeline.name = self.name
        run.pipeline.task = self.task

        run.dataset = Bunch()
        run.dataset.id = self.dataset.id
        run.dataset.name = self.dataset.object.name

        run.model = model_response
        run.model.id = self.model.id
        run.model.name = self.model.object.name

        run.metrics = scores

        run.time = Bunch()
        run.time.start = start_time
        run.time.end = end_time
        run.time.duration = end_time - start_time

        return run

    def __instantiate(self, arguments: Bunch):
        self.type = 'pipeline'
        self.name = arguments.name
        self.description = arguments.description
        self.task = arguments.task

        # convert dataset to config format
        self.dataset = Bunch()
        if isinstance(arguments.dataset, Dataset):
            self.dataset.id = arguments.dataset.module_id
            self.dataset.version = arguments.dataset.version
            self.dataset.object = arguments.dataset
        else:
            raise ValueError('Invalid dataset instance')

        # convert model to config format
        self.model = Bunch()
        if isinstance(arguments.model, tuple):
            if isinstance(arguments.model[0], Model):
                self.model.id = arguments.model[0].module_id
                self.model.version = arguments.model[0].version
                self.model.object = arguments.model[0]
            else:
                raise ValueError('Invalid model instance')

            if isinstance(arguments.model[1], dict):
                self.model.parameters = arguments.model[1]
            else:
                raise ValueError('Invalid model arguments')
        else:
            raise ValueError('Invalid model definition')

        # convert metric to config format
        self.metrics = []
        if isinstance(arguments.metrics, list):
            for metric in arguments.metrics:
                self_metric = Bunch()
                self.metrics.append(self_metric)

                if isinstance(metric, tuple):
                    if isinstance(metric[0], Metric):
                        self_metric.id = metric[0].module_id
                        self_metric.version = metric[0].version
                        self_metric.object = metric[0]
                    else:
                        raise ValueError('Invalid metric instance')

                    if isinstance(arguments.model[1], dict):
                        self_metric.parameters = metric[1]
                    else:
                        raise ValueError('Invalid metric arguments')
                else:
                    raise ValueError('Invalid metric definition')
        else:
            raise ValueError('Invalid metric definition')

        # form the directory path
        self.package_path = causal_bench_path(self.schema_name, self.name)

    @staticmethod
    def create(*args, **keywords):
        # parse arguments
        arguments = parse_arguments(args, keywords)

        # create the instance
        pipeline = Pipeline()
        pipeline.__instantiate(arguments)
        return pipeline
