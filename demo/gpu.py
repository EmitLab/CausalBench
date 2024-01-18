def get_gpus():
    gpus = []

    try:
        import GPUtil
        devices = GPUtil.getGPUs()
        for device in devices:
            gpus.append(GPU('NVIDIA', device))
    except:
        pass

    try:
        from pyadl import ADLManager
        devices = ADLManager.getInstance().getDevices()
        for device in devices:
            gpus.append(GPU('AMD', device))
    except:
        pass

    return gpus


class GPU:

    def __init__(self, vendor, device):
        self.vendor = vendor
        self.device = device

    def get_name(self):
        if self.vendor == 'NVIDIA':
            return self.device.name
        elif self.vendor == 'AMD':
            return self.device.adapterName.decode('utf-8')

    def get_memory_used(self):
        print()
        if self.vendor == 'NVIDIA':
            return self.device.memoryUsed
        elif self.vendor == 'AMD':
            return None

    def get_memory_util(self):
        print()
        if self.vendor == 'NVIDIA':
            return self.device.memoryUtil
        elif self.vendor == 'AMD':
            return self.device.getCurrentUsage()
