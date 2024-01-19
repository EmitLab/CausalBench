import sys
import time
from threading import Thread

try:
    import GPUtil
except:
    print('Failed to import "GPUtil" library', file=sys.stderr)

try:
    from pyadl import ADLManager
except:
    print('Failed to import "pyadl" library', file=sys.stderr)


def get_gpus():
    gpus = []

    if 'GPUtil' in sys.modules:
        devices = GPUtil.getGPUs()
        for device in devices:
            gpus.append(GPU('NVIDIA', device))

    if 'pyadl' in sys.modules:
        devices = ADLManager.getInstance().getDevices()
        for device in devices:
            gpus.append(GPU('AMD', device))

    return gpus


def gpu_profiler():
    gpus = get_gpus()
    if len(gpus) > 0:
        return gpus[0].get_name(), gpus[0].get_memory_total(), GPUProfiler(gpus[0])
    return None, None, None


class GPU:

    def __init__(self, vendor, device):
        self.vendor = vendor
        self.device = device

    def get_uuid(self):
        if self.vendor == 'NVIDIA':
            return self.device.uuid
        elif self.vendor == 'AMD':
            return self.device.uuid.decode('utf-8')

    def get_name(self):
        if self.vendor == 'NVIDIA':
            return self.device.name
        elif self.vendor == 'AMD':
            return self.device.adapterName.decode('utf-8')

    def get_memory_used(self):
        if self.vendor == 'NVIDIA':
            return int(self.device.memoryUsed * 1048576)
        elif self.vendor == 'AMD':
            return None

    def get_memory_util(self):
        if self.vendor == 'NVIDIA':
            return self.device.memoryUtil
        elif self.vendor == 'AMD':
            return self.device.getCurrentUsage()

    def get_memory_total(self):
        if self.vendor == 'NVIDIA':
            return self.device.memoryTotal
        elif self.vendor == 'AMD':
            return None

    def refresh(self):
        gpus = get_gpus()
        for gpu in gpus:
            if gpu.get_uuid() == self.get_uuid():
                self.device = gpu.device


class GPUProfiler(Thread):

    def __init__(self, gpu, delay=1):
        super(GPUProfiler, self).__init__()

        self.gpu = gpu
        self.stopped = False
        self.delay = delay

        self.initial = None
        self.peak = None

    def run(self):
        if self.stopped:
            return

        self.gpu.refresh()
        self.initial = self.peak = self.gpu.get_memory_used()

        if self.initial is None or self.peak is None:
            return

        while not self.stopped:
            self.gpu.refresh()
            memory = self.gpu.get_memory_used()

            if memory > self.peak:
                self.peak = memory

            time.sleep(self.delay)

    def stop(self):
        self.stopped = True
        if self.initial is None or self.peak is None:
            return None
        return self.peak - self.initial
