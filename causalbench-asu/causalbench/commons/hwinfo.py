import platform

import psutil
from bunch_py3 import Bunch
from cpuinfo import cpuinfo

from causalbench.commons.disk import Disks
from causalbench.commons.gpu import GPUs


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
    gpus = GPUs()
    response.gpu = Bunch()
    for gpu in gpus.devices:
        response.gpu[gpu.bus] = Bunch()
        response.gpu[gpu.bus].name = gpu.name
        response.gpu[gpu.bus].driver = gpu.driver
        response.gpu[gpu.bus].memory_total = gpu.memory_total

    # disk IO information
    disks: Disks = Disks()
    response.disk = Bunch()
    for name, disk in disks.devices.items():
        response.disk[name] = disk

    # memory information
    response.memory_total = psutil.virtual_memory().total

    # storage information
    response.storage_total = psutil.disk_usage('/').total

    return response
