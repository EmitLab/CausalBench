import copy

import pandas as pd
from bunch_py3 import Bunch


class SpatioTemporalData:

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.index = Bunch()
        self.index.time = None
        self.index.space = None

    @property
    def time(self):
        return self.index.time

    @time.setter
    def time(self, value):
        self.time = value

    @property
    def space(self):
        return self.index.space

    @space.setter
    def space(self, value):
        self.space = value

    def __copy__(self):
        data_object = SpatioTemporalData(self.data)
        data_object.index.time = self.time
        data_object.index.space = self.space
        return data_object
