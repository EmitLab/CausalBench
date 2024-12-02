import json
import logging
import os
import sys
from abc import ABC, abstractmethod
from importlib import resources

import jsonschema
import yaml
from bunch_py3 import bunchify, Bunch
from jsonschema.exceptions import ValidationError

from causalbench.commons.utils import causalbench_version, extract_module, extract_module_temporary


class Module(ABC):

    def __init__(self, module_id: any, version: int | None, zip_file: str | None):
        # set the module ID and schema name
        self.module_id = module_id
        self.version = version
        self.type = self.__class__.__name__.lower()

        # set library version
        self.causalbench = causalbench_version()

        # load the schema
        self.__load_schema()

        # load the module
        self.__load_module(zip_file)

    def __load_schema(self):
        # load schema
        schema_path = str(resources.files(__package__)
                          .joinpath('schema')
                          .joinpath(self.type + '.yaml'))
        with open(schema_path) as f:
            self.schema = yaml.safe_load(f)

    def __load_module(self, zip_file: str):
        # get package
        self.__get_package(zip_file)

        # load from package path
        if self.package_path is not None:
            # load configuration
            config_path = os.path.join(self.package_path, 'config.yaml')
            with open(config_path) as f:
                entries = yaml.safe_load(f)
                entries = bunchify(entries)

            # update object structure
            self.__dict__.update(entries)

            # validate object structure
            self.__validate()

    def __get_package(self, zip_file):
        # load directly from zip file
        if zip_file is not None:
            # extract zip to temporary directory
            self.package_path = extract_module_temporary(zip_file)

        # load using module ID and version
        elif self.module_id is not None and self.version is not None:
            self.package_path = extract_module(self.module_id, self.version, self.type, self.fetch())

            # # use cached version if available
            # self.package_path = cached_module(self.module_id, self.version, self.type)
            #
            # # cached version is not available
            # if self.package_path is None:
            #     self.package_path = extract_module(self.module_id, self.version, self.type, self.fetch())

        # nothing to load
        else:
            self.package_path = None

    def publish(self, public: bool = False) -> bool:
        if self.module_id is not None and self.version is not None:
            choice = input(f'Are you sure you want to overwrite existing version of {self.type}? [y/N] ')
            if choice.strip() not in ['y', 'Y']:
                return False

        if public:
            choice = input(f'Are you sure you want to publish {self.type} as public? [y/N] ')
            if choice.strip() not in ['y', 'Y']:
                public = False

        return self.save(self.__getstate__(), public)

    def __validate(self):
        config = json.loads(json.dumps(self.__getstate__(), indent=4))
        try:
            jsonschema.validate(instance=config, schema=self.schema)
            logging.debug('Configuration validated successfully')
        except ValidationError as e:
            logging.error(f'Configuration validation error: {e}')
            sys.exit(1)

        cb_ver = causalbench_version()
        if self.causalbench.major != cb_ver.major or self.causalbench.minor != cb_ver.minor:
            logging.error(f'CausalBench {self.causalbench.major}:{self.causalbench.minor} is incompatible with {cb_ver.major}:{cb_ver.minor}')
            sys.exit(1)

        try:
            self.validate()
            logging.debug('Logic validated successfully')
        except Exception as e:
            logging.error(f'Logic validation error: {e}')
            sys.exit(1)

    def __getstate__(self):
        state = bunchify(self.__dict__)

        if 'module_id' in state:
            del state.module_id

        if 'version' in state:
            del state.version

        if 'schema' in state:
            del state.schema

        if 'package_path' in state:
            del state.package_path

        return state

    @abstractmethod
    def validate(self):
        raise NotImplementedError

    @abstractmethod
    def fetch(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def save(self, state: dict, public: bool) -> bool:
        raise NotImplementedError
