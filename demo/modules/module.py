import sys

import yaml
from bunch_py3 import bunchify, Bunch

import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError


class Module:

    def __init__(self, schema_path: str, config_path: str):
        # load schema
        self.schema_path = schema_path
        with open(schema_path) as fp:
            self.schema = json.load(fp)

        # load configuration
        self.config_path = config_path
        with open(config_path) as f:
            entries = yaml.safe_load(f)
            entries = bunchify(entries)

        # validate configuration
        self.validate(entries)

        # expand array of dicts to dict
        self.expand_dicts(entries)

        # set object structure
        self.__dict__.update(entries)

    def expand_dicts(self, entries):
        for item in entries:
            if type(entries[item]) == list:
                if len(entries[item]) > 0 and type(entries[item][0]) == Bunch:
                    values = dict()
                    for value in entries[item]:
                        for k, v in value.items():
                            values[k] = v
                    values = bunchify(values)
                    entries[item] = values

            if type(entries[item]) == Bunch:
                self.expand_dicts(entries[item])

    def validate(self, entries):
        config = json.loads(json.dumps(entries))
        try:
            validate(instance=config, schema=self.schema)
            print('Configuration validated successfully', file=sys.stderr)
        except ValidationError as e:
            print(f'Configuration validation error: {e.message}', file=sys.stderr)
