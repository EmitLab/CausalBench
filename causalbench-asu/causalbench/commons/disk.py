import platform
import re
import subprocess
import plistlib

import psutil
from bunch_py3 import Bunch, bunchify
import os


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

            physical_drives[drive_id].usage.used = physical_drives[drive_id].usage.total - physical_drives[
                drive_id].usage.free

            result = subprocess.run(['powershell', '-Command',
                                     f'Get-PhysicalDisk | Select-Object DeviceID, MediaType | Where-Object {{ $_.DeviceID -eq {drive.Index} }}'],
                                    capture_output=True, text=True)
            if 'SSD' in result.stdout:
                physical_drives[drive_id].mediatype = 'SSD'
            elif 'HDD' in result.stdout:
                physical_drives[drive_id].mediatype = 'HDD'
            else:
                physical_drives[drive_id].mediatype = 'Unknown'

            physical_drives[drive_id].fusion = False

        return physical_drives

    @staticmethod
    def get_physical_drives_linux():
        result = subprocess.run(['lsblk', '-P', '-d', '-o', 'NAME,MODEL,ROTA'], stdout=subprocess.PIPE, text=True)
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

            physical_drives[drive_id].fusion = False

        return physical_drives

    @staticmethod
    def get_physical_drives_macos():
        result = subprocess.run(['diskutil', 'list', '-plist'], stdout=subprocess.PIPE, text=True)
        plist = plistlib.loads(result.stdout.encode())

        disks = dict()
        fusion_list = dict()
        for disk in plist['AllDisks']:
            disk_info = subprocess.run(['diskutil', 'info', '-plist', disk], stdout=subprocess.PIPE, text=True)
            disk_plist = plistlib.loads(disk_info.stdout.encode())

            if disk_plist.get('MountPoint') and disk_plist.get('APFSPhysicalStores'):

                for parent in disk_plist.get('APFSPhysicalStores'):
                    parent = parent["APFSPhysicalStore"]
                    if disk_plist.get('Fusion') and parent not in fusion_list:
                        fusion_list[parent] = disk_plist.get('APFSContainerReference')
                    if parent not in disks:
                        disks[parent] = []
                    disks[parent].append(disk)
        physical_drives = Bunch()

        for disk, partitions in disks.items():
            disk_info = subprocess.run(['diskutil', 'info', '-plist', disk], stdout=subprocess.PIPE, text=True)
            disk_plist = plistlib.loads(disk_info.stdout.encode())
            physical_drives[disk] = Bunch()
            physical_drives[disk].parent = disk_plist.get('ParentWholeDisk')

            physical_drives[disk].usage = Bunch()
            physical_drives[disk].usage.total = 0
            physical_drives[disk].usage.used = 0

            for partition in partitions:
                part_info = subprocess.run(['diskutil', 'info', '-plist', partition], stdout=subprocess.PIPE, text=True)
                part_plist = plistlib.loads(part_info.stdout.encode())
                physical_drives[disk].usage.total = part_plist.get('TotalSize')
                physical_drives[disk].usage.used += part_plist.get('CapacityInUse')

            if 'SolidState' in disk_plist:
                if disk_plist.get('SolidState'):
                    physical_drives[disk].mediatype = 'SSD'
                else:
                    physical_drives[disk].mediatype = 'HDD'
            else:
                physical_drives[disk].mediatype = 'Unknown'
        result = dict()
        for name, disk in physical_drives.items():
            if disk.parent not in result.keys():
                result[disk.parent] = Bunch()
                result[disk.parent].mediatype = disk.mediatype
                result[disk.parent].total = 0
                result[disk.parent].used = 0
                if name in fusion_list:
                    result[disk.parent].fusion = fusion_list[name]
                else:
                    result[disk.parent].fusion = None

            result[disk.parent].total = disk.usage.total
            result[disk.parent].used += disk.usage.used

        for disk in result:
            result[disk].free = result[disk].total - result[disk].used
            drive_info = subprocess.run(['diskutil', 'info', '-plist', disk], stdout=subprocess.PIPE, text=True)
            drive_plist = plistlib.loads(drive_info.stdout.encode())
            result[disk].mediaName = drive_plist.get('MediaName')

        return result


class DisksProfiler:

    def __init__(self, disks: Disks):
        self.disks = disks.disk_drives.keys()
        self._usage = self._get_usage()

    def _get_usage(self) -> Bunch:
        usage: dict = psutil.disk_io_counters(perdisk=True)
        usage: dict = {key: {'read_bytes': value.read_bytes, 'write_bytes': value.write_bytes} for key, value in
                       usage.items() if key in self.disks}
        usage: dict = dict(sorted(usage.items()))
        return bunchify(usage)

    @property
    def usage(self) -> Bunch:
        current_usage = self._get_usage()
        usage: dict = dict()
        for key in self._usage.keys():
            usage[key] = dict()
            usage[key]['read_bytes'] = current_usage[key]['read_bytes'] - self._usage[key]['read_bytes']
            usage[key]['write_bytes'] = current_usage[key]['write_bytes'] - self._usage[key]['write_bytes']
        return bunchify(usage)


def get_disks():
    return Disks()


def get_disks_profiler():
    return DisksProfiler(get_disks())


if __name__ == "__main__":
    disk: Disks = get_disks()
    for k, v in disk.disk_drives.items():
        print(k, v)

    profiler: DisksProfiler = DisksProfiler(disk)
    for k, v in profiler.usage.items():
        print(k, v)

    # drives = get_physical_drives()
    # print(drives)
    # for drive in drives:
    #     print(f"Device: {drive['device']}")
    #     print(f"  Model: {drive.get('model', 'Unknown')}")
    #     print(f"  Size: {drive.get('size', 'Unknown')}")
    #     print(f"  Serial Number: {drive.get('serial_number', drive.get('serial', 'Unknown'))}")
    #     print(f"  Total Size: {drive.get('total_size', 'Unknown')} bytes")
    #     print(f"  Used Space: {drive.get('used_space', 'Unknown')} bytes")
    #     print(f"  Free Space: {drive.get('free_space', 'Unknown')} bytes")
    #     print(f"  Interface Type: {drive.get('interface_type', 'N/A')}")
    #     print()

    # usage_before: Bunch = get_usage()
    #
    # with open('C:\\Users\\prata\\Desktop\\out.txt', 'r') as file:
    #     file.read()
    #
    # usage_after: Bunch = get_usage()
    #
    # print(usage_diff(usage_before, usage_after))