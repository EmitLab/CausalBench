import json
import logging
import os
from abc import ABC, abstractmethod
from importlib import resources

import jsonschema
import yaml
from bunch_py3 import bunchify, Bunch
from jsonschema.exceptions import ValidationError

from causalbench.commons.utils import extract_module


class Module(ABC):

    def __init__(self, module_id: int | None, zip_file: str | None, schema_name: str):
        # set the module ID
        self.module_id = module_id
        self.schema_name = schema_name

        # load the schema
        self.__load_schema()

        # load directly from zip file
        if zip_file is not None:
            self.__load_module(zip_file)

        # load using module ID
        elif self.module_id is not None:
            zip_file = self.fetch(self.module_id)
            self.__load_module(zip_file)

        # nothing to load
        else:
            self.__dict__.update(Bunch())

    def __load_schema(self):
        # load schema
        schema_path = str(resources.files(__package__)
                          .joinpath('schema')
                          .joinpath(self.schema_name + '.yaml'))
        with open(schema_path) as f:
            self.schema = yaml.safe_load(f)

    def __load_module(self, zip_file_path: str):
        # extract zip to temporary directory
        self.package_path = extract_module(self.schema_name, zip_file_path)

        # load configuration
        config_path = os.path.join(self.package_path, 'config.yaml')
        with open(config_path) as f:
            entries = yaml.safe_load(f)
            entries = bunchify(entries)

        # set object structure
        self.__dict__.update(entries)

        # validate object structure
        self.__validate()

    def publish(self):
        self.save(self.__getstate__())

    def __validate(self):
        config = json.loads(json.dumps(self.__getstate__()))
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
        # del state.module_id
        del state.schema
        del state.package_path
        return state

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def fetch(self, module_id: int) -> str:
        pass

    @abstractmethod
    def save(self, state: dict) -> bool:
        pass
