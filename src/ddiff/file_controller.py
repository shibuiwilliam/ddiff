import json
from collections import OrderedDict

import yaml
from ruamel.yaml import YAML, add_constructor, resolver


class FileController(object):
    def __init__(
        self,
        file_o: str,
        file_c: str,
    ):
        self.__file_o: str = file_o
        self.__file_c: str = file_c

        self.__data_o: OrderedDict = self.load_file(file=self.__file_o)
        self.__data_c: OrderedDict = self.load_file(file=self.__file_c)

    @property
    def file_o(self) -> str:
        return self.__file_o

    @property
    def file_c(self) -> str:
        return self.__file_c

    @property
    def data_o(self) -> OrderedDict:
        return self.__data_o

    @property
    def data_c(self) -> OrderedDict:
        return self.__data_c

    def load_file(self, file: str) -> OrderedDict:
        if self.__is_yaml(file=file):
            return self.__load_yaml(file=file)
        if self.__is_json(file=file):
            return self.__load_json(file=file)
        raise Exception("File must be a yaml or json")

    def __is_yaml(self, file: str) -> bool:
        try:
            with open(file, "r", encoding="utf-8") as f:
                yaml.safe_load(f)
            return True
        except yaml.YAMLError as _:
            return False

    def __is_json(self, file: str) -> bool:
        try:
            with open(file, "r", encoding="utf-8") as f:
                json.loads(f)
            return True
        except json.JSONDecodeError as _:
            return False

    def __load_yaml(self, file: str) -> OrderedDict:
        add_constructor(
            resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            lambda loader, node: OrderedDict(loader.construct_pairs(node)),
        )

        _yaml = YAML()
        _yaml.default_flow_style = False

        with open(file, "r", encoding="utf-8") as f:
            data = _yaml.load(f)
        return data

    def __load_json(self, file: str) -> OrderedDict:
        with open(file, "r", encoding="utf-8") as f:
            data = json.loads(f, object_pairs_hook=OrderedDict)

        return data
