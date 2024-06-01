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


def causal_bench_path(*path_list):
    path: Path = Path.home().joinpath('.causalbench')
    for path_str in path_list:
        path = path.joinpath(path_str)
    return str(path)


def extract_module(schema_name: str, zip_file: str):
    # form the directory path
    dir_name = os.path.basename(zip_file[:zip_file.rfind('.')])
    dir_path = causal_bench_path(schema_name, dir_name)

    # extract the zip file
    with ZipFile(zip_file, 'r') as zipped:
        zipped.extractall(path=dir_path)

    return dir_path


def package_module(state, package_path: str, entry_point: str = 'config.yaml'):
    zip_name = tempfile.NamedTemporaryFile(delete=True).name
    zip_file = zip_name + '.zip'

    with ZipFile(zip_file, 'w') as zipped:
        if entry_point:
            zipped.writestr(entry_point, yaml.safe_dump(state))

        for root, dirs, files in os.walk(package_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipped_file_path = os.path.relpath(os.path.join(root, file), package_path)
                if zipped_file_path != entry_point:
                    zipped.write(file_path, zipped_file_path)

    return zip_file
