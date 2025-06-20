import json
import platform
import plistlib
import subprocess

import psutil
from bunch_py3 import Bunch, bunchify


class Disks:

    def __init__(self):
        system = platform.system()
        if system == 'Windows':
            self._physical_drives: Bunch = self._physical_drives_windows()
        elif system == 'Linux':
            self._physical_drives: Bunch = self._physical_drives_linux()
        elif system == 'Darwin':
            self._physical_drives: Bunch = self._physical_drives_macos()
        else:
            raise NotImplementedError(f'Unsupported operating system: {system}')

    @property
    def devices(self) -> Bunch:
        return self._physical_drives

    @staticmethod
    def _syscall(*args) -> str:
        result = subprocess.run(*args, capture_output=True, text=True)
        return result.stdout

    def _physical_drives_windows(self):
        import wmi
        c = wmi.WMI()

        physical_drives = Bunch()

        for drive in c.Win32_DiskDrive():
            drive_id = drive.DeviceID.strip('\\\\.\\').replace('PHYSICALDRIVE', 'PhysicalDrive')

            physical_drives[drive_id] = Bunch()

            physical_drives[drive_id].model = drive.Model.strip()

            physical_drives[drive_id].usage = Bunch()
            physical_drives[drive_id].usage.total = 0
            physical_drives[drive_id].usage.free = 0

            for disk in drive.associators(wmi_result_class='Win32_DiskPartition'):
                for partition in disk.associators(wmi_result_class='Win32_LogicalDisk'):
                    physical_drives[drive_id].usage.total += int(partition.Size)
                    physical_drives[drive_id].usage.free += int(partition.FreeSpace)

            physical_drives[drive_id].usage.used = physical_drives[drive_id].usage.total - physical_drives[drive_id].usage.free

            result = self._syscall(['powershell', '-Command', f'Get-PhysicalDisk | Select-Object DeviceID, MediaType | Where-Object {{ $_.DeviceID -eq {drive.Index} }}'])

            if 'SSD' in result:
                physical_drives[drive_id].mediatype = 'SSD'
            elif 'HDD' in result:
                physical_drives[drive_id].mediatype = 'HDD'
            else:
                physical_drives[drive_id].mediatype = 'Unknown'

            physical_drives[drive_id].fusion = None

        return physical_drives

    def _physical_drives_linux(self):
        def recursive_usage(device):
            if 'children' in device:
                for child in device.children:
                    recursive_usage(child)

            elif device.fssize:
                physical_drives[drive_id].usage.total += int(device.fssize)
                physical_drives[drive_id].usage.free += int(device.fsavail)
                physical_drives[drive_id].usage.used += int(device.fsused)

        result = self._syscall(['lsblk', '-S', '-J', '-o', 'NAME,MODEL,ROTA'])
        drives = json.loads(result)
        drives = bunchify(drives)

        physical_drives = Bunch()

        for drive in drives.blockdevices:
            drive_id = drive.name

            physical_drives[drive_id] = Bunch()

            physical_drives[drive_id].model = drive.model.strip()

            result = self._syscall(['lsblk', '-J', '-b', '-o', 'NAME,FSSIZE,FSAVAIL,FSUSED', f'/dev/{drive_id}'])
            device = json.loads(result)
            device = bunchify(device)

            if device.blockdevices:
                physical_drives[drive_id].usage = Bunch()
                physical_drives[drive_id].usage.total = 0
                physical_drives[drive_id].usage.free = 0
                physical_drives[drive_id].usage.used = 0

                device = device.blockdevices[0]
                recursive_usage(device)

            else:
                physical_drives[drive_id].usage = Bunch()
                physical_drives[drive_id].usage.total = None
                physical_drives[drive_id].usage.free = None
                physical_drives[drive_id].usage.used = None

            if not drive.rota:
                physical_drives[drive_id].mediatype = 'SSD'
            else:
                physical_drives[drive_id].mediatype = 'HDD'

            physical_drives[drive_id].fusion = None

        return physical_drives

    def _physical_drives_macos(self):
        result = self._syscall(['diskutil', 'list', '-plist'])
        plist = plistlib.loads(result.encode())

        # map containers to partitions
        partitions = dict()  # partition to container mapping
        fusions = dict()  # partition to container mapping (for fusion drives)

        for disk in plist['AllDisks']:
            result = self._syscall(['diskutil', 'info', '-plist', disk])
            disk_plist = plistlib.loads(result.encode())

            if disk_plist.get('MountPoint'):
                if disk_plist.get('APFSPhysicalStores'):
                    for partition in disk_plist.get('APFSPhysicalStores'):
                        partition = partition['APFSPhysicalStore']

                        if partition not in partitions:
                            partitions[partition] = []
                        partitions[partition].append(disk)

                        if disk_plist.get('Fusion') and partition not in fusions:
                            fusions[partition] = disk_plist.get('APFSContainerReference')

                else:
                    partitions[disk] = []

        # map partitions to drives
        physical_partitions = Bunch()

        for partition, containers in partitions.items():
            result = self._syscall(['diskutil', 'info', '-plist', partition])
            partition_plist = plistlib.loads(result.encode())

            physical_partitions[partition] = Bunch()

            physical_partitions[partition].parent = partition_plist.get('ParentWholeDisk')

            physical_partitions[partition].usage = Bunch()
            physical_partitions[partition].usage.total = partition_plist.get('TotalSize')
            physical_partitions[partition].usage.used = 0

            if partition_plist.get('FreeSpace'):
                physical_partitions[partition].usage.used = physical_partitions[partition].usage.total - partition_plist.get('FreeSpace')

            else:
                for container in containers:
                    result = self._syscall(['diskutil', 'info', '-plist', container])
                    container_plist = plistlib.loads(result.encode())
                    physical_partitions[partition].usage.used += container_plist.get('CapacityInUse')

        # aggregate partition usage for drives
        physical_drives = Bunch()

        for partition_id, partition in physical_partitions.items():
            device_id = partition.parent

            if device_id not in physical_drives.keys():
                physical_drives[device_id] = Bunch()

                physical_drives[device_id].usage = Bunch()
                physical_drives[device_id].usage.total = 0
                physical_drives[device_id].usage.used = 0

            physical_drives[device_id].usage.total += partition.usage.total
            physical_drives[device_id].usage.used += partition.usage.used

        # drive information
        for device_id, physical_drive in physical_drives.items():
            physical_drive.usage.free = physical_drive.usage.total - physical_drive.usage.used

            result = self._syscall(['diskutil', 'info', '-plist', device_id])
            drive_plist = plistlib.loads(result.encode())

            physical_drive.model = drive_plist.get('MediaName').strip()

            if 'SolidState' in drive_plist:
                if drive_plist.get('SolidState'):
                    physical_drive.mediatype = 'SSD'
                else:
                    physical_drive.mediatype = 'HDD'
            else:
                physical_drive.mediatype = 'Unknown'

            if device_id in fusions:
                physical_drives[device_id].fusion = fusions[device_id]
            else:
                physical_drives[device_id].fusion = None

        return physical_drives


class DisksProfiler:

    def __init__(self, disks: Disks = None):
        if disks is None:
            disks = Disks()
        self.disks = disks.devices.keys()
        self._usage = self._get_usage()

    def _get_usage(self) -> Bunch:
        usage: dict = psutil.disk_io_counters(perdisk=True)
        usage: dict = {key: {'read_bytes': value.read_bytes, 'write_bytes': value.write_bytes} for key, value in usage.items() if key in self.disks}
        usage: dict = dict(sorted(usage.items()))
        return bunchify(usage)

    @property
    def usage(self) -> Bunch:
        current_usage = self._get_usage()
        usage: dict = dict()
        for key in self.disks:
            usage[key] = dict()
            usage[key]['read_bytes'] = current_usage[key]['read_bytes'] - self._usage[key]['read_bytes']
            usage[key]['write_bytes'] = current_usage[key]['write_bytes'] - self._usage[key]['write_bytes']
        return bunchify(usage)
