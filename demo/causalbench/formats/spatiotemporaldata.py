import pandas as pd
from bunch_py3 import Bunch


class SpatioTemporalData:

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self._index = Bunch()
        self._index.target = None
        self._index.time = None
        self._index.space = None

    @property
    def time(self):
        return self._index.time
    
    @property
    def target(self):
        return self._index.target
    
    @target.setter
    def target(self, value):
        self.target = value

    @time.setter
    def time(self, value):
        self.time = value

    @property
    def space(self):
        return self._index.space

    @space.setter
    def space(self, value):
        self.space = value

    def update_index(self, data: Bunch):
        if 'index' in data:
            index_dict = {}
            for name, col in data.index.items():
                index_col = data.columns[col]
                if data.headers:
                    index = index_col.header
                else:
                    index = self.data.columns[index_col.position]
                index_dict[name] = index
            self.index = index_dict

    @property
    def index(self) -> dict[str, str]:
        return self._index

    @index.setter
    def index(self, index: dict[str, str]):
        for name, col in index.items():
            if name in self._index:
                self._index[name] = col
            else:
                raise IndexError(f'Invalid index: "{name}"')

    def __copy__(self):
        data_object = SpatioTemporalData(self.data)
        data_object._index.time = self.time
        data_object._index.space = self.space
        data_object._index.target = self.target
        return data_object
