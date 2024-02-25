import pandas as pd
import numpy as np


class SpatioTemporalData:

    def __init__(self, data: pd.DataFrame, time: str | int = None, space: str | int = None):
        self.data = data
        self.time = time
        self.space = space
