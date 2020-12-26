import json
import os
from collections import OrderedDict
from typing import Dict

import ruamel.yaml
import yaml
from ruamel.yaml import YAML, add_constructor, resolver

from ddiff.utils import random_phrase


def export_to_yaml(output_filepath: str, dict_diff: Dict):
    if output_filepath.endswith("/"):
        basename = random_phrase(n=6)
        filename = f"{basename}.yaml"
        filepath = os.path.join(output_filepath, filename)
    elif not output_filepath.endswith(".yaml") and not output_filepath.endswith(".yml"):
        raise ValueError("Output filepath must be directory or must have yaml extension")
    else:
        filepath = output_filepath

    with open(filepath, "w") as f:
        yaml.dump(dict_diff, f)
    print(f"exported diffs as yaml to {filepath}")


def export_to_json(output_filepath: str, dict_diff: OrderedDict):
    if output_filepath.endswith("/"):
        basename = random_phrase(n=6)
        filename = f"{basename}.json"
        filepath = os.path.join(output_filepath, filename)
    elif not output_filepath.endswith(".json"):
        raise ValueError("Output filepath must be directory or must have json extension")
    else:
        filepath = output_filepath

    with open(filepath, "w") as f:
        json.dump(dict_diff, f, indent=4)
    print(f"exported diffs as json to {filepath}")


class FileLoader(object):
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
