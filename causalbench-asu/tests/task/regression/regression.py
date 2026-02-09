import pandas as pd

from causalbench.formats import SpatioTemporalData
from causalbench.modules.task import AbstractTask


class Regression(AbstractTask):

    def helpers(self) -> any:
        return Helpers

    def model_data_inputs(self) -> dict[str, type]:
        return {'data': SpatioTemporalData}

    def metric_data_inputs(self) -> dict[str, type]:
        return {'ground_truth': SpatioTemporalData}

    def metric_model_inputs(self) -> dict[str, type]:
        return {'prediction': SpatioTemporalData}


class Helpers:

    @staticmethod
    def get_target(data: SpatioTemporalData) -> pd.Series:
        return data.data[data.target]
    
    @staticmethod
    def set_target(data: SpatioTemporalData, target: pd.Series):
        data.data[data.target] = target
