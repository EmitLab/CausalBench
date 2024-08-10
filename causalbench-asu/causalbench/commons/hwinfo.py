import platform

import psutil
from bunch_py3 import Bunch
from cpuinfo import cpuinfo

from causalbench.commons.gpu import gpu_info


def hwinfo() -> Bunch:
    response = Bunch()

    # platform information
    response.platform = Bunch()
    response.platform.name = platform.platform()
    response.platform.architecture = platform.architecture()[0]

    # CPU information
    response.cpu = Bunch()
    response.cpu.name = cpuinfo.get_cpu_info()['brand_raw']
    response.cpu.architecture = cpuinfo.get_cpu_info()['arch']

    # GPU information
    gpu = gpu_info()
    response.gpu = Bunch()
    response.gpu.name = gpu[0]
    response.gpu.driver = gpu[1]
    response.gpu.memory_total = gpu[2]

    # memory information
    response.memory_total = psutil.virtual_memory().total

    # storage information
    response.storage_total = psutil.disk_usage('/').total

    return response
