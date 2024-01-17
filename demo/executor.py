import functools
import os
import platform
import shutil
import tempfile
import time
import tracemalloc
from importlib.metadata import version
from importlib.util import module_from_spec, spec_from_file_location

import cpuinfo
import pipreqs.pipreqs as pipreqs
import psutil


def execute(module_path, func_name, /, *args, **keywords) -> dict:
    # load module
    spec = spec_from_file_location('module', module_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    # get function
    func = getattr(module, func_name)

    # define callable function
    newfunc = functools.partial(func, *args, **keywords)

    # get start time
    start = time.time_ns()

    # start memory trace
    tracemalloc.start()

    # execute the function
    output = newfunc()

    # get peak traced memory
    _, memory = tracemalloc.get_traced_memory()

    # end memory trace
    tracemalloc.stop()

    # get the end time
    end = time.time_ns()

    # calculate the execution duration
    duration = end - start

    # get python information
    python = platform.python_version()

    # get imports
    imports = get_imports(module_path)

    # get platform information
    system_platform = platform.platform()

    # get processor information
    processor = cpuinfo.get_cpu_info()['brand_raw']

    # get architecture information
    architecture = platform.machine()

    # get virtual memory information
    virtual = psutil.virtual_memory().total

    # get storage information
    storage = psutil.disk_usage('/').total

    # form the response
    response = {
        'output': output,
        'duration': duration,
        'memory': memory,
        'python': python,
        'imports': imports,
        'platform': system_platform,
        'processor': processor,
        'architecture': architecture,
        'virtual': virtual,
        'storage': storage
    }

    return response


def get_imports(module_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        # set up paths
        file_name = os.path.basename(module_path)
        temp_path = os.path.join(temp_dir, file_name)

        # copy file to a temporary directory
        shutil.copy2(module_path, temp_path)

        # get names of packages
        candidates = pipreqs.get_all_imports(temp_dir)
        candidates = pipreqs.get_pkg_names(candidates)

        # get versions of packages
        imports = {candidate: version(candidate) for candidate in candidates}

        return imports
