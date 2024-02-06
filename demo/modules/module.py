import json
import logging
import os
from abc import ABC, abstractmethod
from importlib import resources

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
        schema_string = resources.files(__package__).joinpath('schema').joinpath(schema_name + '.json').read_text()
        self.schema = json.loads(schema_string)

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
    def publish(self) -> bool:
        pass
