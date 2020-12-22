import json
import yaml
from ruamel.yaml import YAML, add_constructor, resolver
from collections import OrderedDict


class FileController(object):
    def __init__(self, file_0: str, file_1: str):
        self.__file_0: str = file_0
        self.__file_1: str = file_1

        self.__data_0: OrderedDict = self.load_file(file=self.__file_0)
        self.__data_1: OrderedDict = self.load_file(file=self.__file_1)

    @property
    def data_0(self) -> OrderedDict:
        return self.__data_0

    @property
    def data_1(self) -> OrderedDict:
        return self.__data_1

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
