import time
from enum import Enum
from pathlib import Path

import pandas as pd
from rapidfuzz import process, fuzz


class DeviceType(Enum):
    CPU = 'cpu'
    GPU = 'gpu'


def load(device_type: DeviceType, file_name: str) -> pd.DataFrame:
    # Path to cache
    path: Path = Path('geekbench').joinpath(device_type.value).joinpath(file_name)

    # Check if already cached
    if path.exists():
        return pd.read_csv(path)

    raise FileNotFoundError(f'File {file_name} not found.')


def find_device(device_name: str, device_type: DeviceType, threshold=50):
    # CPU
    if device_type == DeviceType.CPU:
        benchmark_df = load(device_type, 'processors.csv')

    # GPU
    elif device_type == DeviceType.GPU:
        opencl = load(device_type, 'opencl.csv')
        vulkan = load(device_type, 'vulkan.csv')
        metal = load(device_type, 'metal.csv')
        benchmark_df = pd.concat([opencl, vulkan, metal], ignore_index=True)

    # Unknown
    else:
        raise ValueError('Unknown device type')

    # Fuzzy matching
    match, score, index = process.extractOne(device_name, benchmark_df['name'], scorer=fuzz.ratio)

    # Check if the match meets the threshold
    if match and score >= threshold:
        return benchmark_df.iloc[index]

    return None


def main():
    start = time.perf_counter()

    device = find_device('AMD Ryzen 5 5625U with Radeon Graphics', DeviceType.CPU)
    # device = find_device('AMD Radeon (TM) Graphics [gfx90c]', DeviceType.GPU)

    end = time.perf_counter()

    print(device)
    print()
    print(f'{end - start} seconds')


if __name__ == '__main__':
    main()
