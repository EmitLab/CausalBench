import pandas as pd


class SpatioTemporalGraph:

    def __init__(self,
                 data: pd.DataFrame,
                 cause: str | int,
                 effect: str | int,
                 location_cause: str | int,
                 location_effect: str | int,
                 lag: str | int,
                 strength: str | int):
        self.data = data
        self.cause = cause
        self.effect = effect
        self.location_cause = location_cause
        self.location_effect = location_effect
        self.lag = lag
        self.strength = strength
