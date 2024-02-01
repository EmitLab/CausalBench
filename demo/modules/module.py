import json
import logging
import os
from abc import ABC, abstractmethod
from importlib import resources

import yaml
from bunch_py3 import bunchify
from jsonschema import validate
from jsonschema.exceptions import ValidationError


class Module(ABC):

    def __init__(self, module_id: int, schema_path: str):
        if module_id is None:
            self.base_dir = self.instantiate()
            return

        # fetch the module instance from the dataset
        self.base_dir = self.fetch(module_id)
        config_path = os.path.join(self.base_dir, 'config.yaml')

        # load schema
        schema_string = resources.files(__package__).joinpath(schema_path).read_text()
        self.schema = json.loads(schema_string)

        # load configuration
        with open(config_path) as f:
            entries = yaml.safe_load(f)
            entries = bunchify(entries)

        # set object structure
        self.__dict__.update(entries)

        # validate object structure
        self.__validate()

    def __validate(self):
        config = json.loads(json.dumps(self.__dict__))
        try:
            validate(instance=config, schema=self.schema)
            logging.info('Configuration validated successfully')
        except ValidationError as e:
            logging.error(f'Configuration validation error: {e}')

    @abstractmethod
    def instantiate(self) -> str:
        pass

    @abstractmethod
    def fetch(self, module_id: int) -> str:
        pass
