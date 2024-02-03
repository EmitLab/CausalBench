import logging
import os
from pathlib import Path
from zipfile import ZipFile

from bunch_py3 import bunchify

from commons import executor


def parse_arguments(args, keywords):
    # parse the arguments
    if len(args) == 0:
        return bunchify(keywords)
    elif len(args) == 1 and type(args[0]) is dict:
        return bunchify(args[0])
    else:
        logging.error('Invalid arguments')
        return


def execute_and_report(module_path, function_name, /, *args, **keywords):
    try:
        response = executor.execute(module_path, function_name, *args, **keywords)

        print('-' * 80)
        print(f'Module: {module_path}')
        print()

        print('Output:')
        print(response["output"])
        print()

        print(f'Duration: {response["duration"]} nanoseconds')
        print(f'Used Memory: {response["memory"]} bytes')
        if response["gpu_memory"] is None:
            print(f'Used GPU Memory: None')
        else:
            print(f'Used GPU Memory: {response["gpu_memory"]} bytes')
        print()

        print(f'Python: {response["python"]}')
        print(f'Imports: {response["imports"]}')
        print()

        print(f'Platform: {response["platform"]}')
        print(f'Processor: {response["processor"]}')
        print(f'GPU: {response["gpu"]}')
        print(f'Architecture: {response["architecture"]}')
        print(f'Total Memory: {response["memory_total"]} bytes')
        if response["gpu_memory_total"] is None:
            print(f'Total GPU Memory: None')
        else:
            print(f'Total GPU Memory: {response["gpu_memory_total"]} bytes')
        print(f'Total Storage: {response["storage_total"]} bytes')
        print('-' * 80)

        return response["output"]
    except FileNotFoundError as e:
        print(e)
    except AttributeError as e:
        print(e)


def extract_module(schema_name: str, zip_file_path: str):
    # form the directory path
    dir_name = os.path.basename(zip_file_path[:zip_file_path.rfind('.')])
    dir_path = str(Path.home().joinpath('.causalbench').joinpath(schema_name).joinpath(dir_name))

    # extract the zip file
    zip_file = ZipFile(zip_file_path)
    zip_file.extractall(path=dir_path)

    return dir_path
