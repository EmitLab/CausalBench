import functools
import os
import platform
import shutil
import tempfile
import time
import tracemalloc
from importlib.metadata import version
from importlib.util import module_from_spec, spec_from_file_location

import pipreqs.pipreqs as pipreqs
from bunch_py3 import Bunch, bunchify

from causalbench.commons.gpu import gpu_profiler


def execute(module_path, function_name, /, *args, **keywords) -> Bunch:
    # load module
    spec = spec_from_file_location('module', module_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    # get function
    func = getattr(module, function_name)

    # define callable function
    newfunc = functools.partial(func, *args, **keywords)

    # create gpu profiler
    profiler = gpu_profiler()

    # start GPU profiler
    if profiler is not None:
        profiler.start()

    # get start time
    start_time = time.time_ns()

    # start memory trace
    tracemalloc.start()

    # execute the function
    output = newfunc()

    # get peak traced memory
    _, memory = tracemalloc.get_traced_memory()

    # end memory trace
    tracemalloc.stop()

    # get the end time
    end_time = time.time_ns()

    # stop GPU profiler
    gpu_memory = None
    if profiler is not None:
        gpu_memory = profiler.stop()

    # get python information
    python = platform.python_version()

    # get imports
    imports = get_imports(module_path)

    # form the response
    response = Bunch()

    # output
    if isinstance(output, Bunch):
        response.output = output
    elif isinstance(output, dict):
        response.output = bunchify(output)
    else:
        raise ValueError(f'Unexpected output type: {type(output)}')

    # timing
    response.time = Bunch()
    response.time.start = start_time
    response.time.end = end_time
    response.time.duration = end_time - start_time

    # profiling
    response.profiling = Bunch()
    response.profiling.memory = memory
    response.profiling.gpu_memory = gpu_memory
    response.profiling.python = python
    response.profiling.imports = imports

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
        if 'causalbench' in candidates:
            candidates.remove('causalbench')

        # get imports using pipreqs
        imports_pipreqs = pipreqs.get_import_local(candidates)
        candidates = [x for x in candidates if
                      # check if candidate is not in exports
                      x.lower() not in [y for x in imports_pipreqs for y in x['exports']]
                      and
                      # check if candidate is not in package names
                      x.lower() not in [x['name'] for x in imports_pipreqs]]
        imports_pipreqs = {x['name']: x['version'] for x in imports_pipreqs}

        # get imports using importlib
        imports_importlib = {candidate: version(candidate) for candidate in candidates}

        # merge the imports
        imports = {**imports_pipreqs, **imports_importlib}

        # sort the imports
        imports = dict(sorted(imports.items()))

        return imports
