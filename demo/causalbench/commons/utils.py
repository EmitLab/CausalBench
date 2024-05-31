import logging
import os
import tempfile
from pathlib import Path
from zipfile import ZipFile

import yaml
from bunch_py3 import bunchify, Bunch


def parse_arguments(args, keywords):
    # parse the arguments
    if len(args) == 0:
        return bunchify(keywords)
    elif len(args) == 1:
        if isinstance(args[0], dict):
            return bunchify(args[0])
        elif isinstance(args[0], Bunch):
            return args[0]
    else:
        logging.error('Invalid arguments')
        return


def display_run(run):
    print('-' * 80)

    print(f'Task: {run.pipeline.task}')
    print(f'Dataset: {run.dataset.name}')
    print(f'Model: {run.model.name}')

    print('\nMetrics:')
    for metric in run.metrics:
        print(f'    {metric.name}: {metric.output.score}')

    print('-' * 80)

    # print(f'Module: {pipeline_report.mod}')
    # print()
    #
    # print('Output:')
    # print(response["output"])
    # print()
    #
    # print(f'Duration: {response["duration"]} nanoseconds')
    # print(f'Used Memory: {response["memory"]} bytes')
    # if response["gpu_memory"] is None:
    #     print(f'Used GPU Memory: None')
    # else:
    #     print(f'Used GPU Memory: {response["gpu_memory"]} bytes')
    # print()
    #
    # print(f'Python: {response["python"]}')
    # print(f'Imports: {response["imports"]}')
    # print()
    #
    # print(f'Platform: {response["platform"]}')
    # print(f'Processor: {response["processor"]}')
    # print(f'GPU: {response["gpu"]}')
    # print(f'Architecture: {response["architecture"]}')
    # print(f'Total Memory: {response["memory_total"]} bytes')
    # if response["gpu_memory_total"] is None:
    #     print(f'Total GPU Memory: None')
    # else:
    #     print(f'Total GPU Memory: {response["gpu_memory_total"]} bytes')
    # print(f'Total Storage: {response["storage_total"]} bytes')
    # print('-' * 80)
    #
    # return response["output"]


def causal_bench_path(*path_list):
    path: Path = Path.home().joinpath('.causalbench')
    for path_str in path_list:
        path = path.joinpath(path_str)
    return str(path)


def extract_module(schema_name: str, zip_file_path: str):
    # form the directory path
    dir_name = os.path.basename(zip_file_path[:zip_file_path.rfind('.')])
    dir_path = causal_bench_path(schema_name, dir_name)

    # extract the zip file
    zip_file = ZipFile(zip_file_path)
    zip_file.extractall(path=dir_path)

    return dir_path


def package_module(state, package_path: str, entry_point: str = 'config.yaml'):
    zip_name = tempfile.NamedTemporaryFile(delete=True).name
    zip_path = zip_name + '.zip'

    with ZipFile(zip_path, 'w') as zipped:
        if entry_point:
            zipped.writestr(entry_point, yaml.safe_dump(state))

        for root, dirs, files in os.walk(package_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipped_file_path = os.path.relpath(os.path.join(root, file), package_path)
                if zipped_file_path != entry_point:
                    zipped.write(file_path, zipped_file_path)

    return zip_path
