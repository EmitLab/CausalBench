import logging
from datetime import datetime
import requests
import json
from bunch_py3 import Bunch

from demo.causalbench.formats import SpatioTemporalData, SpatioTemporalGraph
from demo.causalbench.modules.dataset import Dataset
from demo.causalbench.modules.metric import Metric
from demo.causalbench.modules.model import Model
from demo.causalbench.modules.module import Module
from demo.causalbench.services.requests import  save_module, fetch_module


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
            #TODO: Set the ID of the dataset also?
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
                # TODO: Set the ID of the dataset also?
                self_metric.object = metric[0]
            elif isinstance(metric[0], int):
                self_metric.id = metric[0]
            self_metric.parameters = metric[1]
            self.metrics.append(self_metric)

        return f'pipeline/{self.name}.zip'

    def validate(self):
        pass

    def fetch(self, module_id: int):
        response = fetch_module(module_id, "pipelines", "downloaded_pipeline.zip")

        return response

    def save(self, state, access_token) -> bool:
        # TODO: Add database call to upload to the server
        input_file_path = None
        # input_file_path = input("Enter the path of pipeline.zip file: ")
        response = save_module(input_file_path, access_token, "pipelines", "pipeline.zip")
        return response

    def execute(self, access_token):
        start = datetime.now()
        # load dataset
        if 'object' in self.dataset:
            dataset = self.dataset.object
        elif 'id' in self.dataset:
            dataset = Dataset(self.dataset.id)
        else:
            logging.error(f'Invalid dataset provided: must be an integer or an object of type {Dataset}')
            return
        print(self.dataset.id,self.model.id)
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
        print(self.model.parameters.items())
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
            
            logging.info("Checked model-metric compatibility")
            # map metric-data parameters
            parameters = Bunch()
            for metric_param, data_param in self_metric.parameters.items():
                parameters[metric_param] = data[data_param]

            # map metric-model parameters
            if self.task in ['discovery.static', 'discovery.temporal']:
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
        response.pipeline.task = self.task

        response.dataset = Bunch()
        response.dataset.id = dataset.module_id
        response.dataset.name = dataset.name

        response.model = model_response
        response.model.id = model.module_id
        response.model.name = model.name

        response.metrics = scores
        end = datetime.now()

        url = 'http://18.116.44.47:8000/instance/env_config'
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "user_id": 4,
            "python_version": "3.11",
            "numpy_version": "1.22",
            "pytorch_version": "2.44",
            "model_version_id": "8"
        }

        api_response = requests.post(url, headers=headers, data=json.dumps(data))

        env_config_id = api_response.text

        # data = {
        #     "user_id": 1,
        #     "gpu_name": "RTX 4090",
        #     "gpu_driver_version": "1",
        #     "gpu_memory": "16GB",
        #     "sys_memory": "64GB",
        #     "os_name": "Windows",
        #     "cpu_name": "Tyzen 7 5900H",
        #     "execution_start_time": "start time",
        #     "execution_end_time": "end time",
        #     "result": "90",
        #     "dataset_version_id": 8,
        #     "model_version_id": 8,
        #     "metric_version_id": 8,
        #     "instance_id":  1,
        #     "env_config_id": 1,
        #     "sys_config_id": 1,
        #     "pipeline_id": 8
        # }

        url = 'http://18.116.44.47:8000/instance/sys_config'
        headers = {
            'Content-Type': 'application/json'
        }

        entry = scores[0]

        data = {
            "user_id": 4,
            "gpu_name": "Unknown" if entry.gpu is None else entry.gpu,
            "gpu_driver_version": "Unknown",
            "gpu_memory": "Unknown" if entry.gpu_memory is None else f"{entry.gpu_memory_total / (1024 ** 3):.2f}GB",
            "sys_memory": f"{entry.memory_total / (1024 ** 3):.2f}GB",
            "os_name": entry.platform.split('-')[0],
            "cpu_name": entry.processor,
        }

        api_response = requests.post(url, headers=headers, data=json.dumps(data))

        sys_config_id = api_response.text

        for entry in scores:
            if entry.name.startswith("accuracy"):
                result = int(entry.output.score * 100)
            else:
                result = f"{int(entry.output.score)}"
            data = {
                "user_id": 4,
                "gpu_name": "Unknown" if entry.gpu is None else entry.gpu,
                "gpu_driver_version": "Unknown",
                "gpu_memory": "Unknown" if entry.gpu_memory is None else f"{entry.gpu_memory_total / (1024 ** 3):.2f}GB",
                "sys_memory": f"{entry.memory_total / (1024 ** 3):.2f}GB",
                "os_name": entry.platform.split('-')[0],
                "cpu_name": entry.processor,
                "execution_start_time": start.strftime('%Y-%m-%d %H:%M:%S'),  # Example start time
                "execution_end_time": end.strftime('%Y-%m-%d %H:%M:%S'),  # Example end time
                "result": f"{result}",
                "dataset_version_id": dataset.module_id,
                "model_version_id": model.module_id,
                "metric_version_id": entry.id,
                "env_config_id": env_config_id,
                "sys_config_id": sys_config_id,
                "instance_id": 1,
                "pipeline_id": self.module_id
            }

            url = 'http://18.116.44.47:8000/runs/'
            headers = {
                'Content-Type': 'application/json'
            }

            api_response = requests.post(url, headers=headers, data=json.dumps(data))


        return response
