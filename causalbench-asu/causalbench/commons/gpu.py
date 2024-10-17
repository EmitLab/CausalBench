import atexit
import logging
import sys
import time
from enum import Enum
from threading import Thread

import pynvml
from bunch_py3 import Bunch
import pyopencl as cl

try:
    from pyadl import ADLManager, ADLDevice
except Exception as e:
    logging.warning(f'Failed to import \'pyadl\' library: {e}')


pynvml_initialized = False

def initialize_pynvml():
    global pynvml_initialized
    if not pynvml_initialized:
        pynvml.nvmlInit()
        atexit.register(pynvml.nvmlShutdown)
        pynvml_initialized = True


class Vendor(Enum):
    NVIDIA = 0x10DE
    AMD = 0x1002


class GPU:

    def __init__(self, vendor: Vendor, device: any, cl_device: cl.Device):
        self.vendor = vendor
        self.device = device
        self.cl_device = cl_device

    @property
    def uuid(self):
        if self.vendor == Vendor.NVIDIA:
            return pynvml.nvmlDeviceGetUUID(self.device)

        elif self.vendor == Vendor.AMD:
            return self.device.uuid.decode('utf-8')

    @property
    def bus(self):
        if self.vendor == Vendor.NVIDIA:
            return pynvml.nvmlDeviceGetPciInfo(self.device).bus

        elif self.vendor == Vendor.AMD:
            return self.device.busNumber

    @property
    def name(self):
        if self.vendor == Vendor.NVIDIA:
            return pynvml.nvmlDeviceGetName(self.device).decode('utf-8')

        elif self.vendor == Vendor.AMD:
            if self.cl_device:
                return f'{self.cl_device.board_name_amd} [{self.cl_device.name}]'
            return self.device.adapterName.decode('utf-8')

    @property
    def memory_used(self):
        if self.vendor == Vendor.NVIDIA:
            return pynvml.nvmlDeviceGetMemoryInfo(self.device).used

        elif self.vendor == Vendor.AMD:
            return None

    @property
    def memory_total(self):
        if self.vendor == Vendor.NVIDIA:
            return pynvml.nvmlDeviceGetMemoryInfo(self.device).total

        elif self.vendor == Vendor.AMD:
            if self.cl_device:
                return self.cl_device.global_mem_size
            return None

    @property
    def utilization(self):
        if self.vendor == Vendor.NVIDIA:
            return pynvml.nvmlDeviceGetUtilizationRates(self.device).gpu

        elif self.vendor == Vendor.AMD:
            return self.device.getCurrentUsage()

    @property
    def driver(self):
        if self.vendor == Vendor.NVIDIA:
            if self.cl_device:
                return self.cl_device.driver_version
            return pynvml.nvmlSystemGetDriverVersion(self.device).decode('utf-8')

        elif self.vendor == Vendor.AMD:
            if self.cl_device:
                return self.cl_device.driver_version
            return None


class GPUs:

    def __init__(self):
        self._devices = []
        nvidia_cl = dict()
        amd_cl = dict()

        # get devices using opencl
        platforms = cl.get_platforms()
        for platform in platforms:
            devices: list[cl.Device] = platform.get_devices()
            for device in devices:
                # NVIDIA
                if device.vendor_id == Vendor.NVIDIA.value:
                    nvidia_cl[device.pci_bus_id_nv] = device

                # AMD
                elif device.vendor_id == Vendor.AMD.value:
                    amd_cl[device.topology_amd.bus] = device

        # get NVIDIA devices using GPUtil
        initialize_pynvml()
        device_count = pynvml.nvmlDeviceGetCount()
        devices: list = [pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(device_count)]
        for index, device in enumerate(devices):
            busNumber = pynvml.nvmlDeviceGetPciInfo(device).bus
            if busNumber in nvidia_cl:
                self._devices.append(GPU(Vendor.NVIDIA, device, nvidia_cl[busNumber]))

        # get AMD devices using pyadl
        if 'pyadl' in sys.modules:
            devices: list[ADLDevice] = ADLManager.getInstance().getDevices()
            for index, device in enumerate(devices):
                if device.busNumber in amd_cl:
                    self._devices.append(GPU(Vendor.AMD, device, amd_cl[device.busNumber]))

    @property
    def devices(self) -> list[GPU]:
        return self._devices


class GPUsProfiler(Thread):

    def __init__(self, gpus: GPUs = None, delay: int=1):
        super(GPUsProfiler, self).__init__()

        if gpus is None:
            gpus = GPUs()

        self.gpus = gpus
        self.stopped = False
        self.delay = delay

        self.idle = dict()
        self.peak = dict()

    def run(self):
        if self.stopped:
            return

        for gpu in self.gpus.devices:
            self.idle[gpu.bus] = self.peak[gpu.bus] = gpu.memory_used

        while not self.stopped:
            for gpu in self.gpus.devices:
                memory = gpu.memory_used

                if memory is not None:
                    if self.idle[gpu.bus] is not None and memory < self.idle[gpu.bus]:
                        self.idle[gpu.bus] = memory
                    if self.peak[gpu.bus] is not None and memory > self.peak[gpu.bus]:
                        self.peak[gpu.bus] = memory

            time.sleep(self.delay)

    def stop(self):
        self.stopped = True

    @property
    def usage(self) -> Bunch:
        usage = Bunch()
        for gpu in self.gpus.devices:
            usage[gpu.bus] = Bunch()
            usage[gpu.bus].idle = self.idle[gpu.bus]
            usage[gpu.bus].peak = self.peak[gpu.bus]
        return usage
