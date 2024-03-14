import pandas as pd
from bunch_py3 import Bunch


class SpatioTemporalGraph:

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self._index = Bunch()
        self._index.cause = self.data.columns[0]
        self._index.effect = self.data.columns[1]
        self._index.location_cause = self.data.columns[2]
        self._index.location_effect = self.data.columns[3]
        self._index.strength = self.data.columns[4]
        self._index.lag = self.data.columns[5]

    @property
    def cause(self):
        return self._index.cause

    @cause.setter
    def cause(self, value):
        self._index.cause = value

    @property
    def effect(self):
        return self._index.effect

    @effect.setter
    def effect(self, value):
        self._index.effect = value

    @property
    def location_cause(self):
        return self._index.location_cause

    @location_cause.setter
    def location_cause(self, value):
        self._index.location_cause = value

    @property
    def location_effect(self):
        return self._index.location_effect

    @location_effect.setter
    def location_effect(self, value):
        self._index.location_effect = value

    @property
    def strength(self):
        return self._index.strength

    @strength.setter
    def strength(self, value):
        self._index.strength = value

    @property
    def lag(self):
        return self._index.lag

    @lag.setter
    def lag(self, value):
        self._index.lag = value

    @property
    def nodes(self) -> list[str]:
        nodes = set()
        nodes.update(self.data[self.cause].tolist())
        nodes.update(self.data[self.effect].tolist())
        return sorted(nodes)

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
        data_object = SpatioTemporalGraph(self.data)
        data_object._index.cause = self.cause
        data_object._index.effect = self.effect
        data_object._index.location_cause = self.location_cause
        data_object._index.location_effect = self.location_effect
        data_object._index.strength = self.strength
        data_object._index.lag = self.lag
        return data_object
