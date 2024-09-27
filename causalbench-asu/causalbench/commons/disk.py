import platform
import re
import subprocess
import plistlib
import time

import psutil
from bunch_py3 import Bunch, bunchify


class Disks:

    def __init__(self):
        system = platform.system()
        if system == 'Windows':
            self._physical_drives: Bunch = self.get_physical_drives_windows()
        elif system == 'Linux':
            self._physical_drives: Bunch = self.get_physical_drives_linux()
        elif system == 'Darwin':
            self._physical_drives: Bunch = self.get_physical_drives_macos()
        else:
            raise NotImplementedError(f'Unsupported operating system: {system}')

    @property
    def disk_drives(self) -> Bunch:
        return self._physical_drives

    @staticmethod
    def get_physical_drives_windows():
        import wmi
        c = wmi.WMI()

        physical_drives = Bunch()

        for drive in c.Win32_DiskDrive():
            drive_id = drive.DeviceID.strip("\\\\.\\").replace("PHYSICALDRIVE", "PhysicalDrive")

            physical_drives[drive_id] = Bunch()

            physical_drives[drive_id].model = drive.Model

            physical_drives[drive_id].usage = Bunch()
            physical_drives[drive_id].usage.total = 0
            physical_drives[drive_id].usage.free = 0

            for disk in drive.associators(wmi_result_class='Win32_DiskPartition'):
                for partition in disk.associators(wmi_result_class='Win32_LogicalDisk'):
                    physical_drives[drive_id].usage.total += int(partition.Size)
                    physical_drives[drive_id].usage.free += int(partition.FreeSpace)

            physical_drives[drive_id].usage.used = physical_drives[drive_id].usage.total - physical_drives[drive_id].usage.free

            result = subprocess.run(['powershell', '-Command', f'Get-PhysicalDisk | Select-Object DeviceID, MediaType | Where-Object {{ $_.DeviceID -eq {drive.Index} }}'], capture_output=True, text=True)

            if 'SSD' in result.stdout:
                physical_drives[drive_id].mediatype = 'SSD'
            elif 'HDD' in result.stdout:
                physical_drives[drive_id].mediatype = 'HDD'
            else:
                physical_drives[drive_id].mediatype = 'Unknown'

            physical_drives[drive_id].fusion = None

        return physical_drives

    @staticmethod
    def get_physical_drives_linux():
        result = subprocess.run(['lsblk', '-S', '-P', '-d', '-o', 'NAME,MODEL,ROTA'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.splitlines()
        lines = [dict(re.findall(r'(\S+)=(".*?"|\S+)', line)) for line in lines]
        lines = [{k: v.strip('"') for k, v in line.items()} for line in lines]
        drives = bunchify(lines)

        physical_drives = Bunch()

        for drive in drives:
            drive_id = drive.NAME

            physical_drives[drive_id] = Bunch()

            physical_drives[drive_id].model = drive.MODEL

            usage = psutil.disk_usage(f'/dev/{drive_id}')
            physical_drives[drive_id].usage = Bunch()
            physical_drives[drive_id].usage.total = usage.total
            physical_drives[drive_id].usage.free = usage.free
            physical_drives[drive_id].usage.used = usage.used

            if drive.ROTA == '0':
                physical_drives[drive_id].mediatype = 'SSD'
            elif drive.ROTA == '1':
                physical_drives[drive_id].mediatype = 'HDD'
            else:
                physical_drives[drive_id].mediatype = 'Unknown'

            physical_drives[drive_id].fusion = None

        return physical_drives

    @staticmethod
    def get_physical_drives_macos():
        physical_drives = subprocess.run(['diskutil', 'list', '-plist'], stdout=subprocess.PIPE, text=True)
        plist = plistlib.loads(physical_drives.stdout.encode())

        # map containers to partitions
        partitions = dict()  # partition to container mapping
        fusions = dict()     # partition to container mapping (for fusion drives)

        for disk in plist['AllDisks']:
            disk_info = subprocess.run(['diskutil', 'info', '-plist', disk], stdout=subprocess.PIPE, text=True)
            disk_plist = plistlib.loads(disk_info.stdout.encode())

            if disk_plist.get('MountPoint') and disk_plist.get('APFSPhysicalStores'):
                for partition in disk_plist.get('APFSPhysicalStores'):
                    partition = partition['APFSPhysicalStore']

                    if partition not in partitions:
                        partitions[partition] = []
                    partitions[partition].append(disk)

                    if disk_plist.get('Fusion') and partition not in fusions:
                        fusions[partition] = disk_plist.get('APFSContainerReference')

        # map partitions to drives
        physical_partitions = Bunch()

        for partition, containers in partitions.items():
            partition_info = subprocess.run(['diskutil', 'info', '-plist', partition], stdout=subprocess.PIPE, text=True)
            partition_plist = plistlib.loads(partition_info.stdout.encode())

            physical_partitions[partition] = Bunch()

            physical_partitions[partition].parent = partition_plist.get('ParentWholeDisk')

            physical_partitions[partition].usage = Bunch()
            physical_partitions[partition].usage.total = partition_plist.get('TotalSize')
            physical_partitions[partition].usage.used = 0

            for container in containers:
                container_info = subprocess.run(['diskutil', 'info', '-plist', container], stdout=subprocess.PIPE, text=True)
                container_plist = plistlib.loads(container_info.stdout.encode())
                physical_partitions[partition].usage.used += container_plist.get('CapacityInUse')

        # aggregate partition usage for drives
        physical_drives = dict()

        for partition_id, partition in physical_partitions.items():
            device_id = partition.parent

            if device_id not in physical_drives.keys():
                physical_drives[device_id] = Bunch()

                physical_drives[device_id].total = 0
                physical_drives[device_id].used = 0

            physical_drives[device_id].total += partition.usage.total
            physical_drives[device_id].used += partition.usage.used

        # drive information
        for device_id, physical_drive in physical_drives.items():
            physical_drive.free = physical_drive.total - physical_drive.used

            drive_info = subprocess.run(['diskutil', 'info', '-plist', device_id], stdout=subprocess.PIPE, text=True)
            drive_plist = plistlib.loads(drive_info.stdout.encode())

            physical_drive.model = drive_plist.get('MediaName')

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

    def __init__(self, disks: Disks):
        self.disks = disks.disk_drives.keys()
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


if __name__ == "__main__":
    disk: Disks = Disks()
    for k, v in disk.disk_drives.items():
        print(k, v)

    profiler: DisksProfiler = DisksProfiler(disk)

    time.sleep(5)
    print()

    for k, v in profiler.usage.items():
        print(k, v)
