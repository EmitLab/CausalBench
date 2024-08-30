import platform
import subprocess
import plistlib
import time

import psutil
from bunch_py3 import Bunch, bunchify


def get_usage() -> Bunch:
    usage: dict = psutil.disk_io_counters(perdisk=True)
    usage: dict = {f'\\\\.\\{key}': {'read_bytes': value.read_bytes, 'write_bytes': value.write_bytes} for key, value in usage.items()}
    return bunchify(usage)


def usage_diff(usage_before: Bunch, usage_after: Bunch) -> Bunch:
    usage: dict = dict()
    for key in usage_before.keys():
        usage[key] = dict()
        usage[key]['read_bytes'] = usage_after[key]['read_bytes'] - usage_before[key]['read_bytes']
        usage[key]['write_bytes'] = usage_after[key]['write_bytes'] - usage_before[key]['write_bytes']
    return bunchify(usage)


def get_physical_drives_windows():
    import wmi
    c = wmi.WMI()

    # get physical drives and associate them with partitions
    physical_drives = Bunch()

    for drive in c.Win32_DiskDrive():
        physical_drives[drive.DeviceID] = Bunch()

        physical_drives[drive.DeviceID].model = drive.Model

        physical_drives[drive.DeviceID].usage = Bunch()
        physical_drives[drive.DeviceID].usage.total = 0
        physical_drives[drive.DeviceID].usage.free = 0

        for disk in drive.associators(wmi_result_class='Win32_DiskPartition'):
            for partition in disk.associators(wmi_result_class='Win32_LogicalDisk'):
                physical_drives[drive.DeviceID].usage.total += int(partition.Size)
                physical_drives[drive.DeviceID].usage.free += int(partition.FreeSpace)

        physical_drives[drive.DeviceID].usage.used = physical_drives[drive.DeviceID].usage.total - physical_drives[drive.DeviceID].usage.free

        result = subprocess.run(["powershell", "-Command", f"Get-PhysicalDisk | Select-Object DeviceID, MediaType | Where-Object {{ $_.DeviceID -eq {0} }}"], capture_output=True, text=True)
        if 'HDD' in result.stdout:
            physical_drives[drive.DeviceID].mediatype = 'HDD'
        elif 'SSD' in result.stdout:
            physical_drives[drive.DeviceID].mediatype = 'SSD'
        else:
            physical_drives[drive.DeviceID].mediatype = 'Unknown'

    return physical_drives


def get_physical_drives_linux():
    result = subprocess.run(['lsblk', '-d', '-o', 'NAME,MODEL,SIZE,SERIAL'], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.splitlines()
    drives = []
    for line in lines[1:]:
        parts = line.split()
        device = f"/dev/{parts[0]}"
        model = parts[1] if len(parts) > 1 else "Unknown"
        size = parts[2]
        serial = parts[3] if len(parts) > 3 else "Unknown"

        # Get disk usage
        usage = psutil.disk_usage(device)
        total_size = usage.total
        free_space = usage.free
        used_space = usage.used

        drives.append({
            'device': device,
            'model': model,
            'size': size,
            'serial': serial,
            'total_size': total_size,
            'free_space': free_space,
            'used_space': used_space
        })
    return drives


def get_physical_drives_macos():
    result = subprocess.run(['diskutil', 'list', '-plist'], stdout=subprocess.PIPE, text=True)
    plist = plistlib.loads(result.stdout.encode())
    drives = []
    for disk in plist['AllDisks']:
        disk_info = subprocess.run(['diskutil', 'info', '-plist', disk], stdout=subprocess.PIPE, text=True)
        disk_plist = plistlib.loads(disk_info.stdout.encode())
        total_size = disk_plist.get('TotalSize', 'Unknown')
        free_space = disk_plist.get('FreeSpace', 'Unknown')
        used_space = total_size - free_space if isinstance(total_size, int) and isinstance(free_space,
                                                                                           int) else 'Unknown'

        drives.append({
            'device': disk,
            'model': disk_plist.get('Model', 'Unknown'),
            'size': total_size,
            'serial': disk_plist.get('Serial', 'Unknown'),
            'total_size': total_size,
            'free_space': free_space,
            'used_space': used_space
        })
    return drives


def get_physical_drives():
    system = platform.system()
    if system == "Windows":
        return get_physical_drives_windows()
    elif system == "Linux":
        return get_physical_drives_linux()
    elif system == "Darwin":
        return get_physical_drives_macos()
    else:
        raise NotImplementedError(f"Unsupported operating system: {system}")


if __name__ == "__main__":
    drives = get_physical_drives()
    print(drives)
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

    usage_before: Bunch = get_usage()

    with open('C:\\Users\\prata\\Desktop\\out.txt', 'r') as file:
        file.read()

    usage_after: Bunch = get_usage()

    print(usage_diff(usage_before, usage_after))
