import sys

try:
    import GPUtil
except NameError:
    pass

try:
    from pyadl import ADLManager
except NameError:
    pass


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
            return self.device.memoryUsed
        elif self.vendor == 'AMD':
            return None

    def get_memory_util(self):
        if self.vendor == 'NVIDIA':
            return self.device.memoryUtil
        elif self.vendor == 'AMD':
            return self.device.getCurrentUsage()
