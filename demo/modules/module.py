import json
import logging
import os
from abc import ABC, abstractmethod
from importlib import resources

import yaml
from bunch_py3 import bunchify, Bunch
from jsonschema import validate
from jsonschema.exceptions import ValidationError


class Module(ABC):

    def __init__(self, module_id: int, schema_name: str):
        if module_id is None:
            return

        # fetch the module instance from the dataset
        self.base_dir = self.fetch(module_id)
        config_path = os.path.join(self.base_dir, 'config.yaml')

        # load schema
        schema_string = resources.files(__package__).joinpath('schema').joinpath(schema_name + '.json').read_text()
        self.schema = json.loads(schema_string)

        # load configuration
        with open(config_path) as f:
            entries = yaml.safe_load(f)
            entries = bunchify(entries)

        # set object structure
        self.__dict__.update(entries)

        # validate object structure
        self.__validate()

    def create(self, *args, **keywords):
        # parse the arguments
        if len(args) == 0:
            arguments = bunchify(keywords)
        elif len(args) == 1 and type(args[0]) is dict:
            arguments = bunchify(args[0])
        else:
            logging.error('Invalid arguments')
            return

        # create the object
        self.base_dir = self.instantiate(arguments)

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
    def instantiate(self, args: Bunch) -> str:
        pass

    @abstractmethod
    def fetch(self, module_id: int) -> str:
        pass
