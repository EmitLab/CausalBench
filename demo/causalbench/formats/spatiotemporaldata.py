import pandas as pd


class SpatioTemporalData:

    def __init__(self, data: pd.DataFrame, time: str | int = None, space: str | int = None):
        self.data = data
        self.time = time
        self.space = space
