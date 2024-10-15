# GPUtil (https://github.com/anderskm/gputil)
# Stripped down version of GPUtil with added support for retrieving bus information
#
#
# LICENSE
#
# MIT License
#
# Copyright (c) 2017 anderskm
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from subprocess import Popen, PIPE
from distutils import spawn
import os
import platform


class GPU:
    def __init__(self, ID, uuid, busNumber, load, memoryTotal, memoryUsed, memoryFree, driver, gpu_name, serial, display_mode, display_active, temp_gpu):
        self.id = ID
        self.uuid = uuid
        self.busNumber = busNumber
        self.load = load
        self.memoryUtil = float(memoryUsed) / float(memoryTotal)
        self.memoryTotal = memoryTotal
        self.memoryUsed = memoryUsed
        self.memoryFree = memoryFree
        self.driver = driver
        self.name = gpu_name
        self.serial = serial
        self.display_mode = display_mode
        self.display_active = display_active
        self.temperature = temp_gpu


def safeFloatCast(strNumber):
    try:
        number = float(strNumber)
    except ValueError:
        number = float('nan')
    return number


def getGPUs() -> list[GPU]:
    if platform.system() == "Windows":
        # If the platform is Windows and nvidia-smi could not be found from the environment path,
        # try to find it from system drive with default installation path
        nvidia_smi = spawn.find_executable('nvidia-smi')
        if nvidia_smi is None:
            nvidia_smi = "%s\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe" % os.environ['systemdrive']
    else:
        nvidia_smi = "nvidia-smi"

    # Get ID, processing and memory utilization for all GPUs
    try:
        p = Popen([nvidia_smi,
                   "--query-gpu=index,uuid,pci.bus,utilization.gpu,memory.total,memory.used,memory.free,driver_version,name,gpu_serial,display_active,display_mode,temperature.gpu",
                   "--format=csv,noheader,nounits"], stdout=PIPE)
        stdout, stderror = p.communicate()
    except:
        return []

    output = stdout.decode('UTF-8')

    # Parse output
    lines = output.split(os.linesep)

    gpus = []

    for g in range(len(lines) - 1):
        line = lines[g]
        vals = line.split(', ')

        deviceIds = int(vals[0])
        uuid = vals[1]
        busNumber = int(vals[2], 16)
        gpuUtil = safeFloatCast(vals[3]) / 100
        memTotal = safeFloatCast(vals[4])
        memUsed = safeFloatCast(vals[5])
        memFree = safeFloatCast(vals[6])
        driver = vals[7]
        gpu_name = vals[8]
        serial = vals[9]
        display_active = vals[10]
        display_mode = vals[11]
        temp_gpu = safeFloatCast(vals[12])

        gpus.append(GPU(deviceIds, uuid, busNumber, gpuUtil, memTotal, memUsed, memFree, driver, gpu_name, serial, display_mode, display_active, temp_gpu))

    return gpus
