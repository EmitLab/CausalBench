import logging
import os
import requests

from bunch_py3 import Bunch

from causalbench.commons import executor
from causalbench.commons.utils import parse_arguments
from causalbench.modules.module import Module


class Model(Module):

    def __init__(self, model_id: int = None):
        super().__init__(model_id, 'model')

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def validate(self):
        if self.task == 'discovery.static':
            if 'data' not in self.inputs:
                raise ValueError('Input does not include a \'data\' field')
            if 'prediction' not in self.outputs:
                raise ValueError('Output does not include a \'prediction\' field')

            # TODO: Perform logical validation of the structure
        pass

    def fetch(self, model_id: int):
        # TODO: Replace with database call to download zip and obtain path
        filename = None
        print(f"MODULE: {model_id}")
        url = f'http://127.0.0.1:8000/model_version/download/{model_id}/'
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
                filename = 'downloaded_model.zip'
            
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f'Download successful, saved as {filename}')
        else:
            print(f'Failed to download file: {response.status_code}')
            print(response.text)

        return filename
        if model_id == 0:
            return 'model/pc.zip'
        elif model_id == 1:
            return 'model/ges.zip'
        elif model_id == 2:
            return 'model/lingam.zip'
        elif model_id == 3:
            return 'model/ermirmcfcminst.zip'

    def save(self, state) -> bool:
        # TODO: Add database call to upload to the server
        input_file_path = input("Enter the path of model.zip file: ")
        input_file_path = "/home/abhinavgorantla/emitlab/causal_bench/CausalBench/zipfiles/model.zip"
        print(f"Saving model!")

        url = 'http://127.0.0.1:8000/model_version/upload/'
        headers = {
            # 'Content-Type': 'application/json'
        }
        files = {
            'file': ('model.zip', open(input_file_path, 'rb'), 'application/zip')
        }

        response = requests.post(url, headers=headers, files=files)
        print(response.status_code)
        print(response.text)

    def execute(self, *args, **keywords):
        # parse the arguments
        arguments: Bunch = parse_arguments(args, keywords)

        # form the proper file path
        file_path = os.path.join(self.package_path, self.path)

        # map the model arguments
        model_args = {}
        print(self.task)
        if self.task == 'discovery.static':
            model_args[self.inputs.data.id] = arguments.data

        elif self.task == 'discovery.temporal':
            model_args[self.inputs.data.id] = arguments.data

        elif self.task == 'discovery.spatiotemporal':
            model_args[self.inputs.data.id] = arguments.data
            model_args[self.inputs.space.id] = arguments.space if 'space' in arguments else None

        elif self.task == 'classification':
            model_args[self.inputs.data.id] = arguments.data
            model_args[self.inputs.target.id] = arguments.target
        else:
            raise TypeError(f'Invalid task type: {self.task}')

        # execute the model
        response = executor.execute(file_path, 'execute', **model_args)

        # map the outputs
        output = Bunch()
        for key, data in self.outputs.items():
            output[key] = response.output[data.id]
        response.output = output

        logging.info('Executed model successfully')

        return response
