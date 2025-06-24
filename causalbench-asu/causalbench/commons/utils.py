import atexit
import logging
import os
import re
import shutil
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urlparse
from zipfile import ZipFile

import requests
import yaml
from bunch_py3 import bunchify, Bunch


def causalbench_version() -> Bunch:
    ver = Bunch()
    ver.major, ver.minor, ver.build = re.split(r'\.|(?<=\d)(?=\D)', version('causalbench-asu'))
    return ver


def parse_arguments(args, keywords):
    # parse the arguments
    if len(args) == 0:
        return bunchify(keywords)
    elif len(args) == 1:
        if isinstance(args[0], Bunch):
            return args[0]
        elif isinstance(args[0], dict):
            return bunchify(args[0])
    else:
        logging.error('Invalid arguments')
        sys.exit(1)


def causal_bench_path(*path_list) -> str:
    path: Path = Path.home().joinpath('.causalbench')
    for path_str in path_list:
        path = path.joinpath(str(path_str))
    return str(path)


def cached_module(module_id, version, module_type: str) -> str:
    # form the directory path
    dir_path = causal_bench_path(module_type, module_id, version)

    # check if directory exists
    if os.path.isdir(dir_path):
        return dir_path


def extract_module(module_id, version, module_type: str, zip_file: str) -> str:
    # form the directory path
    dir_path = causal_bench_path(module_type, module_id, version)

    # extract the zip file
    extract_zip(zip_file, dir_path)

    return dir_path


def extract_module_temporary(zip_file: str) -> str:
    # form the directory path
    dir_path = tempfile.TemporaryDirectory().name
    atexit.register(lambda: shutil.rmtree(dir_path))

    # extract the zip file
    extract_zip(zip_file, dir_path)

    return dir_path


def package_module(state, package_path: str, entry_point: str = 'config.yaml') -> str:
    zip_file = tempfile.NamedTemporaryFile(delete=True, suffix='.zip').name
    atexit.register(lambda: os.remove(zip_file))

    with ZipFile(zip_file, 'w') as zipped:
        if entry_point:
            zipped.writestr(entry_point, yaml.safe_dump(state, sort_keys=False, indent=4))

        if package_path is not None:
            for root, dirs, files in os.walk(package_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipped_file_path = os.path.relpath(os.path.join(root, file), package_path)
                    if zipped_file_path != entry_point:
                        zipped.write(file_path, zipped_file_path)

    return zip_file


def extract_zip(source, out_dir='.'):
    parsed = urlparse(source)
    is_url = parsed.scheme in ('http', 'https')

    if is_url:
        tmp_path = None
        try:
            with requests.get(source, stream=True) as r:
                r.raise_for_status()
                with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
                    for chunk in r.iter_content(chunk_size=8192):
                        tmp_file.write(chunk)
                    tmp_path = tmp_file.name

            with ZipFile(tmp_path, 'r') as zf:
                zf.extractall(out_dir)

        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    else:
        with ZipFile(source, 'r') as zf:
            zf.extractall(out_dir)
