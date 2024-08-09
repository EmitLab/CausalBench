import os
from abc import ABC, abstractmethod
from importlib.util import spec_from_file_location, module_from_spec

from bunch_py3 import Bunch

from causalbench.modules.module import Module


class AbstractTask(ABC):

    @abstractmethod
    def helpers(self) -> any:
        raise NotImplementedError

    @abstractmethod
    def model_data_inputs(self) -> dict[str, type]:
        raise NotImplementedError

    @abstractmethod
    def metric_data_inputs(self) -> dict[str, type]:
        raise NotImplementedError

    @abstractmethod
    def metric_model_inputs(self) -> dict[str, type]:
        raise NotImplementedError


class Task(Module):

    def __init__(self, module_id: str = None, zip_file: str = None):
        super().__init__(module_id, 0, zip_file, 'task')

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def validate(self):
        # TODO: Perform logical validation of the structure
        pass

    def fetch(self):
        # return fetch_module('Task',
        #                     self.module_id,
        #                     self.version,
        #                     'task',
        #                     'downloaded_task.zip')

        if self.module_id == 'discovery.static':
            return 'task/discovery.static.zip'
        if self.module_id == 'discovery.temporal':
            return 'task/discovery.temporal.zip'

    def save(self, state, public: bool) -> bool:
        # TODO: Save the task
        pass

    def load(self) -> AbstractTask:
        # form the proper file path
        file_path = os.path.join(self.package_path, self.path)

        # load the module
        spec = spec_from_file_location('module', file_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        # create an instance of the task
        class_name = getattr(module, self.class_name)
        task: AbstractTask = class_name()

        return task
