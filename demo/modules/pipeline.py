import logging
from zipfile import ZipFile

import yaml
from bunch_py3 import Bunch

from modules.dataset import Dataset
from modules.metric import Metric
from modules.model import Model
from modules.module import Module


class Pipeline(Module):

    def __init__(self, module_id: int = None):
        super().__init__(module_id, 'pipeline')

    def instantiate(self, arguments: Bunch):
        self.type = 'pipeline'
        self.name = arguments.name
        self.task = arguments.task
        self.dataset = arguments.dataset
        self.model = arguments.model
        self.metrics = arguments.metrics

        return f'pipeline/{self.name}.zip'

    def validate(self):
        pass

    def fetch(self, module_id: int):
        # TODO: Replace with database call to download zip and obtain path
        if module_id == 0:
            return 'pipeline/pipeline0.zip'

    def publish(self) -> bool:
        with ZipFile(self.package_path, 'w') as zipped:
            zipped.writestr('config.yaml', yaml.dump(self.__dict__))
        return True

    def execute(self):
        # dataset
        if type(self.dataset) == Dataset:
            dataset = self.dataset
        elif type(self.dataset) == int:
            dataset = Dataset(self.dataset)
        else:
            logging.error(f'Invalid dataset provided: must be an integer or an object of type {Dataset}')
            return

        data = dataset.load()
        X = data.file1
        ground_truth = data.file2

        # model
        if type(self.model) == Model:
            model = self.model
        elif type(self.model) == int:
            model = Model(self.model)
        else:
            logging.error(f'Invalid model provided: must be an integer or an object of type {Model}')
            return

        result = model.execute(data=X)
        matrix = result.prediction

        # metrics
        scores = []
        for metric in self.metrics:
            if type(metric) == Metric:
                pass
            elif type(metric) == int:
                metric = Metric(metric)
            else:
                logging.error(f'Invalid metric provided: must be an integer or an object of type {Metric}')
                return

            result = metric.evaluate(ground_truth=ground_truth, prediction=matrix)
            scores.append((metric.module_id, metric.name, result.score))

        return PipelineResult(pipeline=(self.module_id, self.name),
                              dataset=(dataset.module_id, dataset.name),
                              model=(model.module_id, model.name),
                              metrics=scores)


class PipelineResult:

    def __init__(self,
                 pipeline: tuple,
                 dataset: tuple,
                 model: tuple,
                 metrics: list[tuple]):
        self.pipeline = pipeline
        self.dataset = dataset
        self.model = model
        self.metrics = metrics
