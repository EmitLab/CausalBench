import json
import logging
import os.path
import sys
import tempfile

import requests

from causalbench import access_token


def save_module(input_file_path, api_base, output_file_name):
    url = f'http://18.116.44.47:8000/{api_base}/upload/'
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    files = {
        'file': (output_file_name, open(input_file_path, 'rb'), 'application/zip')
    }

    response = requests.post(url, headers=headers, files=files)

    print(f'{response.status_code}: {response.text}', file=sys.stderr)

    return response.status_code == 200


def save_run(run):
    url = 'http://18.116.44.47:8000/instance/env_config'
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {access_token}"
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
    #     "pipeline_id": 8
    # }

    url = 'http://18.116.44.47:8000/instance/sys_config'
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
            "pipeline_id": run.pipeline.id
        }

        url = 'http://18.116.44.47:8000/runs/'
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        print(f'{response.status_code}: {response.text}', file=sys.stderr)

        return response.status_code == 200


def fetch_module(module_id, base_api, output_file_name):
    url = f'http://18.116.44.47:8000/{base_api}/download/{module_id}/'
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
            file_name = output_file_name

        file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'Module {module_id} - Download successful, saved as {file_path}', file=sys.stderr)

        return file_path

    else:
        logging.error(f'Module {module_id} - Failed to download file: {response.status_code}')
        logging.error(response.text)

        return None
