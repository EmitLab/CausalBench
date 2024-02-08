import json
import logging
import os
from abc import ABC, abstractmethod
from importlib import resources
from zipfile import ZipFile

import jsonschema
import yaml
from bunch_py3 import bunchify, Bunch
from jsonschema.exceptions import ValidationError

from commons.utils import parse_arguments, extract_module


class Module(ABC):

    def __init__(self, module_id: int, schema_name: str):
        # set the module ID
        self.module_id = module_id

        # load schema
        schema_path = str(resources.files(__package__).joinpath('schema').joinpath(schema_name + '.yaml'))
        with open(schema_path) as f:
            self.schema = yaml.safe_load(f)

        if module_id is not None:
            # create temporary directory
            zip_file_path = self.fetch(module_id)
            self.package_path = extract_module(schema_name, zip_file_path)

            # load configuration
            config_path = os.path.join(self.package_path, 'config.yaml')
            with open(config_path) as f:
                entries = yaml.safe_load(f)
                entries = bunchify(entries)

            # set object structure
            self.__dict__.update(entries)

            # validate object structure
            self.__validate()

    def create(self, *args, **keywords):
        # parse the arguments
        arguments = parse_arguments(args, keywords)

        # create the object
        self.package_path = self.instantiate(arguments)

        # validate object structure
        self.__validate()

    def publish(self):
        self.save(self.__getstate__())

    def __validate(self):
        config = json.loads(json.dumps(self.__dict__))
        try:
            jsonschema.validate(instance=config, schema=self.schema)
            logging.info('Configuration validated successfully')
        except ValidationError as e:
            logging.error(f'Configuration validation error: {e}')

        try:
            self.validate()
            logging.info('Logic validated successfully')
        except Exception as e:
            logging.error(f'Logic validation error: {e}')

    def __getstate__(self):
        state = bunchify(self.__dict__)
        del state['module_id']
        del state['schema']
        del state['package_path']
        return state

    @abstractmethod
    def instantiate(self, arguments: Bunch) -> str:
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def fetch(self, module_id: int) -> str:
        pass

    @abstractmethod
    def save(self, state: dict) -> bool:
        pass
