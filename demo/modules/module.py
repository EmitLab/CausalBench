import json
import logging
from abc import ABC, abstractmethod
from importlib import resources

import yaml
from bunch_py3 import bunchify
from jsonschema import validate
from jsonschema.exceptions import ValidationError


class Module(ABC):

    def __init__(self, module_id: int, schema_path: str):
        if module_id is None:
            self.instantiate()
            return

        config_path = self.fetch(module_id)

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
    def instantiate(self):
        pass

    @abstractmethod
    def fetch(self, module_id: int) -> str:
        pass
