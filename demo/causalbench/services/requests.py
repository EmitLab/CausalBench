import json
import logging
import os.path
import sys
import tempfile

import requests
from bunch_py3 import bunchify

from causalbench import access_token


def save_module(module_type, module_id, version, public, input_file, api_base, default_output_file):
    visibility = "private"
    if public:
        visibility = "public"
    if module_id is None:
        url = f'https://www.causalbench.org/api/{api_base}/upload?visibility={visibility}'
    elif module_id is not None and version is None:
        url = f'https://www.causalbench.org/api/{api_base}/upload/{module_id}?visibility={visibility}'
    else:
        url = f'https://www.causalbench.org/api/{api_base}/upload/{module_id}/{version}?visibility={visibility}'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    files = {
        'file': (default_output_file, open(input_file, 'rb'), 'application/zip')
    }

    response = requests.post(url, headers=headers, files=files)
    data = bunchify(response.json())

    if response.status_code == 200:
        print(f'{module_type} published: ID={data.id}, Version={data.version_num}', file=sys.stderr)
        return data.id, data.version_num

    else:
        print(f'Failed to publish {module_type.lower()}: {response.status_code}', file=sys.stderr)


def save_run(run):
    url = 'https://www.causalbench.org/api/instance/env_config'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    data = {
        "user_id": 4,
        "python_version": "3.11",
        "numpy_version": "1.22",
        "pytorch_version": "2.44",
        "model_version_id": str(run.model.id),
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
    #     "scenario_id": 8
    # }

    url = 'https://www.causalbench.org/api/instance/sys_config'
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {access_token}"
    }

    entry = run.metrics[0]

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

    for entry in run.metrics:
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
            "execution_start_time": run.time.start.strftime('%Y-%m-%d %H:%M:%S'),  # Example start time
            "execution_end_time": run.time.end.strftime('%Y-%m-%d %H:%M:%S'),  # Example end time
            "result": f"{result}",
            "dataset_version_id": run.dataset.id,
            "model_version_id": run.model.id,
            "metric_version_id": entry.id,
            "env_config_id": env_config_id,
            "sys_config_id": sys_config_id,
            "instance_id": 1,
            "scenario_id": run.scenario.id
        }

        url = 'https://www.causalbench.org/api/runs/'
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        data = bunchify(response.json())

        if response.status_code == 200:
            print(f'Run published: ID={data.id}', file=sys.stderr)
            return data.id

        else:
            print(f'Failed to publish run: {response.status_code} - {data.msg}', file=sys.stderr)


def fetch_module(module_type, module_id, version, base_api, default_output_file):
    url = f'https://www.causalbench.org/api/{base_api}/download/{module_id}/{version}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Extract filename from the Content-Disposition header if available
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            file_name = content_disposition.split('filename=')[-1].strip('"')
        else:
            # Fallback to a default name if the header is not present
            file_name = default_output_file

        file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'{module_type} {module_id} - Download successful, saved as {file_path}', file=sys.stderr)

        return file_path

    else:
        logging.error(f'{module_type} {module_id} - Failed to download file: {response.status_code}')
        logging.error(response.text)

        return None
