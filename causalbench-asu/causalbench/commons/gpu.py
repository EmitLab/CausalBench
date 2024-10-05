import logging
import sys
import time
from enum import Enum
from threading import Thread

from bunch_py3 import Bunch
import pyopencl as cl
from pyadl import ADLManager, ADLDevice
from causalbench.commons import GPUtil


class Vendor(Enum):
    NVIDIA = 0x10DE
    AMD = 0x1002


class GPU:

    def __init__(self, vendor: Vendor, device: any, cl_device: cl.Device):
        self.vendor = vendor
        self.device = device
        self.cl_device = cl_device

    @property
    def id(self):
        if self.vendor == Vendor.NVIDIA:
            return self.device.id

        elif self.vendor == Vendor.AMD:
            return self.device.adapterIndex

    @property
    def uuid(self):
        if self.vendor == Vendor.NVIDIA:
            return self.device.uuid

        elif self.vendor == Vendor.AMD:
            return self.device.uuid.decode('utf-8')

    @property
    def bus(self):
        if self.vendor == Vendor.NVIDIA:
            return self.device.busId

        elif self.vendor == Vendor.AMD:
            return self.device.busNumber

    @property
    def name(self):
        if self.vendor == Vendor.NVIDIA:
            return self.device.name

        elif self.vendor == Vendor.AMD:
            if self.cl_device:
                return f'{self.cl_device.board_name_amd} [{self.cl_device.name}]'
            return self.device.adapterName.decode('utf-8')

    @property
    def memory_used(self):
        if self.vendor == Vendor.NVIDIA:
            return int(self.device.memoryUsed * 1048576)

        elif self.vendor == Vendor.AMD:
            return None

    @property
    def memory_util(self):
        if self.vendor == Vendor.NVIDIA:
            return self.device.memoryUtil

        elif self.vendor == Vendor.AMD:
            return self.device.getCurrentUsage()

    @property
    def memory_total(self):
        if self.vendor == Vendor.NVIDIA:
            if self.cl_device:
                return self.cl_device.global_mem_size
            return int(self.device.memoryTotal * 1048576)

        elif self.vendor == Vendor.AMD:
            if self.cl_device:
                return self.cl_device.global_mem_size
            return None

    @property
    def driver(self):
        if self.vendor == Vendor.NVIDIA:
            if self.cl_device:
                return self.cl_device.driver_version
            return self.device.driver

        elif self.vendor == Vendor.AMD:
            if self.cl_device:
                return self.cl_device.driver_version
            return None

    def refresh(self):
        if self.vendor == Vendor.NVIDIA:
            devices = GPUtil.getGPUs()
            for device in devices:
                if self.device.uuid == device.uuid:
                    self.device = device
                    break

        elif self.vendor == Vendor.AMD:
            pass


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
        if 'GPUtil' in sys.modules:
            devices: list[GPUtil.GPU] = GPUtil.getGPUs()
            for index, device in enumerate(devices):
                self._devices.append(GPU(Vendor.NVIDIA, device, nvidia_cl[device.busId]))

        # get AMD devices using pyadl
        if 'pyadl' in sys.modules:
            devices: list[ADLDevice] = ADLManager.getInstance().getDevices()
            for index, device in enumerate(devices):
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
            gpu.refresh()
            self.idle[gpu.id] = self.peak[gpu.id] = gpu.memory_used

        while not self.stopped:
            for gpu in self.gpus.devices:
                gpu.refresh()
                memory = gpu.memory_used

                if memory is not None:
                    if self.idle[gpu.id] is not None and memory < self.idle[gpu.id]:
                        self.idle[gpu.id] = memory
                    if self.peak[gpu.id] is not None and memory > self.peak[gpu.id]:
                        self.peak[gpu.id] = memory

            time.sleep(self.delay)

    def stop(self):
        self.stopped = True

    @property
    def usage(self) -> Bunch:
        usage = Bunch()
        for gpu in self.gpus.devices:
            usage[gpu.id] = Bunch()
            usage[gpu.id].idle = self.idle[gpu.id]
            usage[gpu.id].peak = self.peak[gpu.id]
        return usage
