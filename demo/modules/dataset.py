import yaml
from bunch_py3 import bunchify

from modules.module import Module


class Dataset(Module):

    def __init__(self, config_path: str):
        super().__init__('../schema/dataset.json', config_path)

    def load(self):
        print(self.files.dataset.columns.sex.vals[0])
        pass


data = Dataset('../data/config.yaml')
data.load()
