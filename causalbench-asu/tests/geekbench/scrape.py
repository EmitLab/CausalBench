import requests
from enum import Enum
from pathlib import Path

import pandas as pd


class DeviceType(Enum):
    CPU = 'cpu'
    GPU = 'gpu'


def scrape(url: str, device_type: DeviceType, file_name: str):
    # Path to cache
    path: Path = Path('geekbench').joinpath(device_type.value).joinpath(file_name)

    # Scrape Geekbench
    response = requests.get(url)
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(data['devices'])

    # Save to file
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def main():
    scrape('https://browser.geekbench.com/processor-benchmarks.json', DeviceType.CPU, 'processors.csv')

    scrape('https://browser.geekbench.com/opencl-benchmarks.json',  DeviceType.GPU, 'opencl.csv')
    scrape('https://browser.geekbench.com/vulkan-benchmarks.json', DeviceType.GPU, 'vulkan.csv')
    scrape('https://browser.geekbench.com/metal-benchmarks.json', DeviceType.GPU, 'metal.csv')


if __name__ == '__main__':
    main()
