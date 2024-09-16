from causalbench.modules import Dataset
import pytest
import pandas as pd

dataset_web = Dataset(module_id=2, version=1)
fetched_web = dataset_web.fetch()
data_web = Dataset(zip_file=fetched_web)
files_web = data_web.load()
assert isinstance(files_web["file1"].data, pd.DataFrame), "Dataset from causalbench could not be fetched."


dataset = Dataset(zip_file='data/abalone.zip')
files = dataset.load()
assert isinstance(files["file1"].data, pd.DataFrame), "Local data could not be extracted."


#dataset1.publish(public=False)
