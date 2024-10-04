import logging
import sys
import time
from threading import Thread

from bunch_py3 import Bunch, bunchify

try:
    import GPUtil
except Exception as e:
    logging.warning(f'Failed to import \'GPUtil\' library: {e}')

try:
    from pyadl import ADLManager
except Exception as e:
    logging.warning(f'Failed to import \'pyadl\' library: {e}')


class GPU:

    def __init__(self, vendor, device):
        self.vendor = vendor
        self.device = device

    @property
    def id(self):
        if self.vendor == 'NVIDIA':
            return self.device.id
        elif self.vendor == 'AMD':
            return self.device.adapterIndex

    @property
    def uuid(self):
        if self.vendor == 'NVIDIA':
            return self.device.uuid
        elif self.vendor == 'AMD':
            return self.device.uuid.decode('utf-8')

    @property
    def name(self):
        if self.vendor == 'NVIDIA':
            return self.device.name
        elif self.vendor == 'AMD':
            return self.device.adapterName.decode('utf-8')

    @property
    def memory_used(self):
        if self.vendor == 'NVIDIA':
            return int(self.device.memoryUsed * 1048576)
        elif self.vendor == 'AMD':
            return None

    @property
    def memory_util(self):
        if self.vendor == 'NVIDIA':
            return self.device.memoryUtil
        elif self.vendor == 'AMD':
            return self.device.getCurrentUsage()

    @property
    def memory_total(self):
        if self.vendor == 'NVIDIA':
            return int(self.device.memoryTotal * 1048576)
        elif self.vendor == 'AMD':
            return None

    @property
    def driver(self):
        if self.vendor == 'NVIDIA':
            return self.device.driver
        elif self.vendor == 'AMD':
            return None

    def refresh(self):
        if self.vendor == 'NVIDIA':
            devices = GPUtil.getGPUs()
            for device in devices:
                if self.device.uuid == device.uuid:
                    self.device = device
                    break

        elif self.vendor == 'AMD':
            pass


class GPUs:

    def __init__(self):
        self._devices = []

        if 'GPUtil' in sys.modules:
            devices = GPUtil.getGPUs()
            for device in devices:
                self._devices.append(GPU('NVIDIA', device))

        if 'pyadl' in sys.modules:
            devices = ADLManager.getInstance().getDevices()
            for device in devices:
                self._devices.append(GPU('AMD', device))

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
