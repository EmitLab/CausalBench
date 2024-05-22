import logging
import requests
import json
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
        filename = None
        print(f"MODULE: {module_id}")
        url = f'http://127.0.0.1:8000/pipelines/download/{module_id}/'
        headers = {
            'User-Agent': 'insomnia/2023.5.8'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Extract filename from the Content-Disposition header if available
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                filename = content_disposition.split('filename=')[-1].strip('"')
            else:
                # Fallback to a default name if the header is not present
                filename = 'downloaded_pipeline.zip'
            
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f'Download successful, saved as {filename}')
        else:
            print(f'Failed to download file: {response.status_code}')
            print(response.text)
        if module_id == 0:
            return 'pipeline/pipeline0.zip'
        elif module_id == 1:
            return 'pipeline/pipeline1.zip'
        elif module_id == 2:
            return 'pipeline/pipeline2.zip'

    def save(self, state) -> bool:
        # TODO: Add database call to upload to the server
        # input_file_path = input("Enter the path of dataset.zip file: ")
        input_file_path = "/home/abhinavgorantla/emitlab/causal_bench/CausalBench/zipfiles/pipeline.zip"
        print(f"Saving pipeline {self.module_id}!")

        url = 'http://127.0.0.1:8000/pipelines/upload/'
        headers = {
            # 'Content-Type': 'application/json'
        }
        files = {
            'file': ('pipeline.zip', open(input_file_path, 'rb'), 'application/zip')
        }

        response = requests.post(url, headers=headers, files=files)
        print(response.status_code)
        print(response.text)

    def execute(self):
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

        url = 'http://127.0.0.1:8000/instance/env_config'
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "user_id": 1,
            "python_version": "3.11",
            "numpy_version": "1.22",
            "pytorch_version": "2.44",
            "model_version_id": "8"
        }

        api_response = requests.post(url, headers=headers, data=json.dumps(data))

        env_config_id = api_response.text

        url = 'http://127.0.0.1:8000/instance/sys_config'
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "user_id": 1,
            "gpu_name": "Nvidia RTX 3060",
            "gpu_driver_version": "12.11.2",
            "gpu_memory": "8GB",
            "sys_memory": "8GB",
            "os_name": "Windows",
            "cpu_name": "AMD RYzen 5 5600H"
        }

        api_response = requests.post(url, headers=headers, data=json.dumps(data))

        sys_config_id = api_response.text

        url = 'http://127.0.0.1:8000/runs/'
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "user_id": 1,
            "gpu_name": "RTX 4090",
            "gpu_driver_version": "1",
            "gpu_memory": "16GB",
            "sys_memory": "64GB",
            "os_name": "Windows",
            "cpu_name": "Tyzen 7 5900H",
            "execution_start_time": "start time",
            "execution_end_time": "end time",
            "result": "90",
            "dataset_version_id": 8,
            "model_version_id": 8,
            "metric_version_id": 8,
            "instance_id":  1,
            "env_config_id": 1,
            "sys_config_id": 1,
            "pipeline_id": 8
        }

        api_response = requests.post(url, headers=headers, data=json.dumps(data))

        return response
