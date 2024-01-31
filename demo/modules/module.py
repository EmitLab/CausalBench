import logging
from importlib import resources

import yaml
from bunch_py3 import bunchify

import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError


class Module:

    def __init__(self, schema_path: str, config_path: str):
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
