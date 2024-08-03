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
from causalbench.modules.task import Task
from causalbench.services.requests import save_module, fetch_module


class Scenario:

    def __init__(self, task: Task, dataset: Dataset, mapping: Bunch, model: Model, metrics: list[Metric]):
        self.task = task
        self.dataset = dataset
        self.mapping = mapping
        self.model = model
        self.metrics = metrics

    def execute(self) -> Run:
        # execution start time
        start_time = datetime.now()

        # load the task
        task = self.task.load()

        # load data
        data = self.dataset.load()

        # # update indices
        # if 'files' in self.dataset:
        #     for file, data_object in data.items():
        #         if file in self.dataset.files:
        #             if isinstance(data_object, SpatioTemporalData):
        #                 data_object.update_index(self.dataset.files[file])
        #             if isinstance(data_object, SpatioTemporalGraph):
        #                 data_object.update_index(self.dataset.files[file])

        # check model compatibility
        if self.model.task != self.task.module_id:
            raise TypeError(f'Model "{self.model.name}" not compatible with task "{self.task.module_id}"')

        # check metric compatibility
        for metric in self.metrics:
            if metric.task != self.task.module_id:
                raise TypeError(f'Metric "{metric.name}" not compatible with task "{self.task.module_id}"')

        # map model parameters
        parameters: Bunch = Bunch()
        parameters.update(self.map_parameters(task.model_data_inputs(), data, self.mapping))
        parameters.helpers = task.helpers()

        # execute the model
        model_response: Bunch = self.model.execute(parameters)

        # metrics
        scores = []
        for self_metric in self.metrics:
            # map metric parameters
            parameters: Bunch = Bunch()
            parameters.update(self.map_parameters(task.metric_data_inputs(), data, self.mapping))
            parameters.update(self.map_parameters(task.metric_model_inputs(), model_response.output))
            parameters.helpers = task.helpers()

            # execute the metric
            metric_response = self_metric.evaluate(parameters)
            metric_response.id = self_metric.module_id
            metric_response.name = self_metric.name
            scores.append(metric_response)

        # execution end time
        end_time = datetime.now()

        # form the response
        run = Run()

        run.dataset = Bunch()
        run.dataset.id = self.dataset.module_id
        run.dataset.name = self.dataset.name

        run.model = model_response
        run.model.id = self.model.module_id
        run.model.name = self.model.name

        run.metrics = scores

        run.time = Bunch()
        run.time.start = start_time
        run.time.end = end_time
        run.time.duration = end_time - start_time

        return run

    @staticmethod
    def map_parameters(fields: dict[str, type], data: Bunch, mapping: Bunch = None) -> Bunch:
        # if no mapping specified, assume the input and output names are same
        if mapping is None:
            mapping = {field: field for field in fields}

        # map data to fields using mapping
        parameters: Bunch = Bunch()

        for field, datatype in fields.items():
            # check if mapping is specified
            if field not in mapping:
                raise ValueError(f'Mapping does not specify a "{field}" field')

            # check if specified mapping exists
            if mapping[field] not in data:
                raise ValueError(f'Parameter "{mapping[field]}" for field "{field}" does not exist')

            # check if datatype of mapped field is correct
            if not isinstance(data[mapping[field]], datatype):
                raise ValueError(f'Parameter "{mapping[field]}" for field "{field}" is not of type {datatype}')

            # perform mapping
            parameters[field] = data[mapping[field]]

        return parameters
