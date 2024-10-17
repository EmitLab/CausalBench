import time

from bunch_py3 import Bunch

from causalbench.modules.dataset import Dataset
from causalbench.modules.metric import Metric
from causalbench.modules.model import Model
from causalbench.modules.task import Task


class Scenario:

    def __init__(self,
                 task: Task,
                 dataset: tuple[Dataset, Bunch],
                 model: tuple[Model, Bunch],
                 metrics: list[tuple[Metric, Bunch]]):
        self.task = task
        self.dataset = dataset
        self.model = model
        self.metrics = metrics

    def execute(self) -> Bunch:
        # execution start time
        start_time = time.time_ns()

        # load the task
        task = self.task.load()

        # load data
        data = self.dataset[0].load()

        # # update indices
        # if 'files' in self.dataset[0]:
        #     for file, data_object in data.items():
        #         if file in self.dataset[0].files:
        #             if isinstance(data_object, SpatioTemporalData):
        #                 data_object.update_index(self.dataset[0].files[file])
        #             if isinstance(data_object, SpatioTemporalGraph):
        #                 data_object.update_index(self.dataset[0].files[file])

        # check model compatibility
        if self.model[0].task != self.task.module_id:
            raise TypeError(f'Model "{self.model[0].name}" not compatible with task "{self.task.module_id}"')

        # check metric compatibility
        for metric in self.metrics:
            if metric[0].task != self.task.module_id:
                raise TypeError(f'Metric "{metric[0].name}" not compatible with task "{self.task.module_id}"')

        # map model parameters
        parameters: Bunch = Bunch()
        parameters.update(self.map_parameters(task.model_data_inputs(), data, self.dataset[1]))
        parameters.update(self.model[1])
        parameters.helpers = task.helpers()

        # execute the model
        model_response: Bunch = self.model[0].execute(parameters)

        # metrics
        scores = []
        for self_metric in self.metrics:
            # map metric parameters
            parameters: Bunch = Bunch()
            parameters.update(self.map_parameters(task.metric_data_inputs(), data, self.dataset[1]))
            parameters.update(self.map_parameters(task.metric_model_inputs(), model_response.output))
            parameters.update(self_metric[1])
            parameters.helpers = task.helpers()

            # execute the metric
            metric_response = self_metric[0].evaluate(parameters)
            metric_response.id = self_metric[0].module_id
            metric_response.version = self_metric[0].version
            metric_response.name = self_metric[0].name
            metric_response.hyperparameters = self_metric[1]
            scores.append(metric_response)

        # execution end time
        end_time = time.time_ns()

        # form the response
        response = Bunch()

        # dataset
        response.dataset = Bunch()
        response.dataset.id = self.dataset[0].module_id
        response.dataset.version = self.dataset[0].version
        response.dataset.name = self.dataset[0].name

        # model
        response.model = model_response
        response.model.id = self.model[0].module_id
        response.model.version = self.model[0].version
        response.model.name = self.model[0].name
        response.model.hyperparameters = self.model[1]

        # metrics
        response.metrics = scores

        # timing
        response.time = Bunch()
        response.time.start = start_time
        response.time.end = end_time
        response.time.duration = end_time - start_time

        return response

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
