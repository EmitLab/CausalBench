import logging
from datetime import datetime

from bunch_py3 import Bunch, bunchify

from causalbench.commons.utils import parse_arguments, package_module, causal_bench_path
from causalbench.formats import SpatioTemporalData, SpatioTemporalGraph
from causalbench.modules import Scenario
from causalbench.modules.dataset import Dataset
from causalbench.modules.metric import Metric
from causalbench.modules.model import Model
from causalbench.modules.module import Module
from causalbench.modules.run import Run
from causalbench.modules.task import Task, AbstractTask
from causalbench.services.requests import save_module, fetch_module


class Context(Module):

    def __init__(self, module_id: int = None, version: int = None, zip_file: str = None):
        super().__init__(module_id, version, zip_file, 'context')

    def __getstate__(self):
        state = super().__getstate__()

        if 'datasets' in state:
            for dataset in state.datasets:
                if 'object' in dataset:
                    del dataset.object

        if 'models' in state:
            for model in state.models:
                if 'object' in model:
                    del model.object

        if 'metrics' in state:
            for metric in state.metrics:
                if 'object' in metric:
                    del metric.object

        return state

    def validate(self):
        # TODO: To be implemented
        pass

    def fetch(self):
        return fetch_module('Context',
                            self.module_id,
                            self.version,
                            'contexts',
                            'downloaded_context.zip')

    def save(self, state) -> bool:
        for dataset in state.datasets:
            if dataset.id is None:
                logging.error('Cannot publish context as it contains unpublished dataset')
                return False

        for model in state.models:
            if model.id is None:
                logging.error('Cannot publish context as it contains unpublished model')
                return False

        for metric in state.metrics:
            if metric.id is None:
                logging.error('Cannot publish context as it contains unpublished metric')
                return False

        zip_file = package_module(state, self.package_path)
        self.module_id = save_module('Context',
                                     self.module_id,
                                     zip_file,
                                     'contexts',
                                     'context.zip')
        return self.module_id is not None

    def execute(self) -> Run | None:
        # execution start time
        start_time = datetime.now()

        # load the task
        task: Task = Task(module_id=self.task)

        # load the datasets
        datasets = []
        for dataset in self.datasets:
            if 'object' not in dataset:
                dataset.object = Dataset(module_id=dataset.id, version=dataset.version)
            datasets.append((dataset.object, dataset.mapping))

        # load the models
        models = []
        for model in self.models:
            if 'object' not in model:
                model.object = Model(module_id=model.id, version=model.version)
            models.append(model.object)

        # load the metrics
        metrics = []
        for metric in self.metrics:
            if 'object' not in metric:
                metric.object = Metric(module_id=metric.id, version=metric.version)
            metrics.append(metric.object)

        # create the scenarios
        scenarios = []
        for dataset in datasets:
            for model in models:
                scenario = Scenario(task, dataset[0], dataset[1], model, metrics)
                scenarios.append(scenario)

        # execute the scenarios
        for scenario in scenarios:
            run: Run = scenario.execute()
            print(run)

        # execution end time
        end_time = datetime.now()

        # load data
        # data = self.dataset.object.load()

        # # update indices
        # if 'files' in self.dataset:
        #     for file, data_object in data.items():
        #         if file in self.dataset.files:
        #             if isinstance(data_object, SpatioTemporalData):
        #                 data_object.update_index(self.dataset.files[file])
        #             if isinstance(data_object, SpatioTemporalGraph):
        #                 data_object.update_index(self.dataset.files[file])

        # # map model-data parameters
        # parameters = {}
        # for model_param, data_param in self.model.parameters.items():
        #     parameters[model_param] = data[data_param]
        #
        # # execute the model
        # model_response: Bunch = self.model.object.execute(parameters)
        #
        # # metrics
        # scores = []
        # for self_metric in self.metrics:
        #     # check model-metric compatibility
        #     if self.model.object.task != self_metric.object.task:
        #         logging.error(f'The model "{self.model.object.name}" and metric "{self_metric.object.name}" are not compatible')
        #         return
        #     logging.info("Checked model-metric compatibility")
        #
        #     # map metric-data parameters
        #     parameters = Bunch()
        #     for metric_param, data_param in self_metric.parameters.items():
        #         parameters[metric_param] = data[data_param]
        #
        #     # map metric-model parameters
        #     if self.task in ['discovery.static', 'discovery.temporal', 'classification']:
        #         parameters.prediction = model_response.output.prediction
        #
        #     # execute the metric
        #     metric_response = self_metric.object.evaluate(parameters)
        #     metric_response.id = self_metric.object.module_id
        #     metric_response.name = self_metric.object.name
        #     scores.append(metric_response)
        #
        # # execution end time
        # end_time = datetime.now()
        #
        # # form the response
        # run = Run()
        #
        # run.scenario = Bunch()
        # run.scenario.id = self.module_id
        # run.scenario.name = self.name
        # run.scenario.task = self.task
        #
        # run.dataset = Bunch()
        # run.dataset.id = self.dataset.id
        # run.dataset.name = self.dataset.object.name
        #
        # run.model = model_response
        # run.model.id = self.model.id
        # run.model.name = self.model.object.name
        #
        # run.metrics = scores
        #
        # run.time = Bunch()
        # run.time.start = start_time
        # run.time.end = end_time
        # run.time.duration = end_time - start_time

        # return run

    def __instantiate(self, arguments: Bunch):
        self.type = 'context'
        self.name = arguments.name
        self.description = arguments.description
        self.task = arguments.task

        # convert datasets to config format
        self.datasets = []
        if isinstance(arguments.datasets, list):
            for dataset in arguments.datasets:
                self_dataset = Bunch()
                self.datasets.append(self_dataset)

                if isinstance(dataset, tuple):
                    # dataset
                    if isinstance(dataset[0], Dataset):
                        self_dataset.id = dataset[0].module_id
                        self_dataset.version = dataset[0].version
                        self_dataset.object = dataset[0]
                    else:
                        raise ValueError('Invalid dataset instance')

                    # data mapping
                    if isinstance(dataset[1], Bunch):
                        self_dataset.mapping = dataset[1]
                    elif isinstance(dataset[1], dict):
                        self_dataset.mapping = bunchify(dataset[1])
                    else:
                        raise ValueError('Invalid data mapping')
                else:
                    raise ValueError('Invalid dataset definition')
        else:
            raise ValueError('Invalid dataset definition')

        # convert models to config format
        self.models = []
        if isinstance(arguments.models, list):
            for model in arguments.models:
                self_model = Bunch()
                self.models.append(self_model)

                if isinstance(model, tuple):
                    # model
                    if isinstance(model[0], Model):
                        self_model.id = model[0].module_id
                        self_model.version = model[0].version
                        self_model.object = model[0]
                    else:
                        raise ValueError('Invalid model instance')

                    # hyperparameters
                    # if isinstance(arguments.model[1], dict):
                    #     self_model.parameters = model[1]
                    # else:
                    #     raise ValueError('Invalid model arguments')
                else:
                    raise ValueError('Invalid model definition')
        else:
            raise ValueError('Invalid model definition')

        # convert metrics to config format
        self.metrics = []
        if isinstance(arguments.metrics, list):
            for metric in arguments.metrics:
                self_metric = Bunch()
                self.metrics.append(self_metric)

                if isinstance(metric, tuple):
                    # metric
                    if isinstance(metric[0], Metric):
                        self_metric.id = metric[0].module_id
                        self_metric.version = metric[0].version
                        self_metric.object = metric[0]
                    else:
                        raise ValueError('Invalid metric instance')

                    # hyperparameters
                    # if isinstance(arguments.model[1], dict):
                    #     self_metric.parameters = metric[1]
                    # else:
                    #     raise ValueError('Invalid metric arguments')
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
        context = Context()
        context.__instantiate(arguments)
        return context
