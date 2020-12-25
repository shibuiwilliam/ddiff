import json
import pprint
from abc import ABCMeta, abstractmethod
from collections import Counter, OrderedDict
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import ruamel.yaml

from ddiff.configurations import OUTPUT_FORMAT, Configurations
from ddiff.utils import print_decorator, random_separator


class DIFFERENCE(Enum):
    DIFFERENT_TYPES = "different types"
    DIFFERENT_VALUES = "different values"
    ARRAY_IN_DIFFERENT_SEQUENCE = "array in different sequence"
    KEY_NOT_IN_FILE = "key not in {}"


class AbstractDifference(metaclass=ABCMeta):
    def __init__(self, path: str, depth: int, file_o: str, file_c: str):
        self.path: str = path
        self.depth: int = depth
        self.file_o: str = file_o
        self.file_c: str = file_c
        self.status: DIFFERENCE

    @abstractmethod
    def pretty_print(self):
        print(f"- {self.status.value}")

    @abstractmethod
    def values(self) -> Dict[str, Union[str, List, None]]:
        return {
            "status": self.status.__class__.__name__,
            self.file_o: "",
            self.file_c: "",
        }


class DifferentTypes(AbstractDifference):
    def __init__(
        self,
        path: str,
        depth: int,
        file_o: str,
        file_c: str,
        file_o_value: Any,
        file_c_value: Any,
        file_o_type: str,
        file_c_type: str,
    ):
        super().__init__(path=path, depth=depth, file_o=file_o, file_c=file_c)
        self.file_o_value: Any = file_o_value
        self.file_c_value: Any = file_c_value
        self.file_o_type: str = file_o_type
        self.file_c_type: str = file_c_type
        self.status: DIFFERENCE = DIFFERENCE.DIFFERENT_TYPES

    def pretty_print(self):
        super(DifferentTypes, self).pretty_print()
        print(f"{Configurations.indent()}{self.file_o}: {self.file_o_type}")
        print(f"{Configurations.indent()}{self.file_c}: {self.file_c_type}")

    def values(self) -> Dict[str, Union[str, List, None]]:
        return {
            "status": self.status.__class__.__name__,
            self.file_o: self.file_o_type,
            self.file_c: self.file_c_type,
        }


class DifferentValues(AbstractDifference):
    def __init__(
        self,
        path: str,
        depth: int,
        file_o: str,
        file_c: str,
        file_o_value: Any,
        file_c_value: Any,
    ):
        super().__init__(path=path, depth=depth, file_o=file_o, file_c=file_c)
        self.file_o_value: Any = file_o_value
        self.file_c_value: Any = file_c_value
        self.status: DIFFERENCE = DIFFERENCE.DIFFERENT_VALUES

    def pretty_print(self):
        super(DifferentValues, self).pretty_print()
        print(f"{Configurations.indent()}{self.file_o}: {self.file_o_value}")
        print(f"{Configurations.indent()}{self.file_c}: {self.file_c_value}")

    def values(self) -> Dict[str, Union[str, List, None]]:
        return {
            "status": self.status.__class__.__name__,
            self.file_o: self.file_o_value,
            self.file_c: self.file_c_value,
        }


class ArrayInDifferentSequence(AbstractDifference):
    def __init__(
        self,
        path: str,
        depth: int,
        file_o: str,
        file_c: str,
        file_o_array: List[Any],
        file_c_array: List[Any],
    ):
        super().__init__(path=path, depth=depth, file_o=file_o, file_c=file_c)
        self.file_o_array: List = file_o_array
        self.file_c_array: List = file_c_array
        self.status: DIFFERENCE = DIFFERENCE.ARRAY_IN_DIFFERENT_SEQUENCE

    def pretty_print(self):
        super(ArrayInDifferentSequence, self).pretty_print()
        print(f"{Configurations.indent()}{self.file_o}: {self.file_o_array}")
        print(f"{Configurations.indent()}{self.file_c}: {self.file_c_array}")

    def values(self) -> Dict[str, Union[str, List, None]]:
        return {
            "status": self.status.__class__.__name__,
            self.file_o: self.file_o_array,
            self.file_c: self.file_c_array,
        }


class KeyNotInFile(AbstractDifference):
    def __init__(
        self,
        path: str,
        depth: int,
        file_o: str,
        file_c: str,
        file_o_value: Any,
    ):
        super().__init__(path=path, depth=depth, file_o=file_o, file_c=file_c)
        self.file_o_value: Any = file_o_value
        self.status: DIFFERENCE = DIFFERENCE.KEY_NOT_IN_FILE

    def pretty_print(self):
        print(f"- {self.status.value.format(self.file_c)}")
        print(f"{Configurations.indent()}{self.file_c}: null")
        print(f"{Configurations.indent()}{self.file_o}: {self.file_o_value}")

    def values(self) -> Dict[str, Union[str, List, None]]:
        return {
            "status": self.status.__class__.__name__,
            self.file_o: self.file_o_value,
            self.file_c: None,
        }


class Ddiff(object):
    def __init__(
        self,
        file_o: str,
        file_c: str,
        data_o: Any,
        data_c: Any,
        output_format: OUTPUT_FORMAT = OUTPUT_FORMAT.DEFAULT,
        indent_key: bool = False,
    ):
        self.file_o = file_o
        self.file_c = file_c
        self.data_o = data_o
        self.data_c = data_c
        self.output_format = output_format
        self.indent_key = indent_key

        self.__diffs: Dict[str, AbstractDifference] = {}

        self.separator = random_separator()

    def __call__(self):
        self.ddiff()

    @property
    def diffs(self) -> Dict:
        return self.__diffs

    @print_decorator()
    def diffs_to_dict(self) -> OrderedDict:
        dict_diff: OrderedDict[str, Dict[str, str]] = OrderedDict()
        for path, diff in self.diffs.items():
            _path = diff.path.replace(self.separator, ".")
            _path = _path[1:]
            dict_diff[_path] = diff.values()
        return dict_diff

    @print_decorator()
    def add_diff(self, path: str, diff: AbstractDifference):
        if path not in self.__diffs.keys():
            self.__diffs[path] = diff

    @print_decorator()
    def pretty_print(self):
        if self.output_format == OUTPUT_FORMAT.DEFAULT:
            self.default_pretty_print()
        elif self.output_format == OUTPUT_FORMAT.YAML:
            odict_diff = self.diffs_to_dict()
            res = ""
            for line in ruamel.yaml.round_trip_dump(
                odict_diff,
                indent=Configurations.indent_size,
                block_seq_indent=3,
            ).splitlines(True):
                res += line[3:]
            print(res)
        elif self.output_format == OUTPUT_FORMAT.JSON:
            odict_diff = self.diffs_to_dict()
            dict_diff = dict(odict_diff)
            print(json.dumps(dict_diff, indent=Configurations.indent_size))

    @print_decorator()
    def default_pretty_print(self):
        sorted_diffs = sorted(self.diffs.values(), key=lambda x: x.depth)
        for diff in sorted_diffs:
            print(f"{Configurations.line_separator}")
            if self.indent_key:
                _path = ""
                for i, p in enumerate(diff.path.split(self.separator)):
                    if i == 0:
                        continue
                    _path += f"{self.key_indent(depth=i-1)}{p}"
            else:
                _path = diff.path.replace(self.separator, ".")
                _path = _path[1:]
            print(_path)
            diff.pretty_print()

    @print_decorator()
    def key_indent(self, depth: int = 0) -> str:
        if depth == 0:
            return ""
        else:
            indent = "  " * (depth - 1) + "└─"
            return f"\n{indent}"

    @print_decorator()
    def _compare_types(
        self,
        path: str,
        file_o: str,
        file_c: str,
        data_o: Any,
        data_c: Any,
        depth: int,
    ) -> bool:
        if type(data_o) != type(data_c):
            self.add_diff(
                path=path,
                diff=DifferentTypes(
                    path=path,
                    depth=depth,
                    file_o=file_o,
                    file_c=file_c,
                    file_o_value=data_o,
                    file_c_value=data_c,
                    file_o_type=type(data_o).__name__,
                    file_c_type=type(data_c).__name__,
                ),
            )
            return False
        return True

    @print_decorator()
    def _compare_values(
        self,
        path: str,
        file_o: str,
        file_c: str,
        data_o: Any,
        data_c: Any,
        depth: int,
    ) -> bool:
        if data_o != data_c:
            self.add_diff(
                path=path,
                diff=DifferentValues(
                    path=path,
                    depth=depth,
                    file_o=file_o,
                    file_c=file_c,
                    file_o_value=data_o,
                    file_c_value=data_c,
                ),
            )
            return False
        return True

    @print_decorator()
    def _compare_array_sequence(
        self,
        path,
        file_o: str,
        file_c: str,
        data_o: List,
        data_c: List,
        depth: int,
    ) -> bool:
        c_0 = Counter(data_o)
        c_1 = Counter(data_c)
        if c_0 == c_1:
            self.add_diff(
                path=path,
                diff=ArrayInDifferentSequence(
                    path=path,
                    depth=depth,
                    file_o=file_o,
                    file_c=file_c,
                    file_o_array=data_o,
                    file_c_array=data_c,
                ),
            )
            return False
        return True

    @print_decorator()
    def _compare_dict(
        self,
        path: str,
        file_o: str,
        file_c: str,
        data_o: Dict,
        data_c: Dict,
        depth: int = 0,
    ):
        for key, _data_o in data_o.items():
            _path = f"{path}{self.separator}{key}"
            if key in data_c.keys():
                self._ddiff(
                    file_o=file_o,
                    file_c=file_c,
                    data_o=_data_o,
                    data_c=data_c[key],
                    path=_path,
                    depth=depth + 1,
                )
            else:
                self.add_diff(
                    path=_path,
                    diff=KeyNotInFile(
                        path=_path,
                        depth=depth,
                        file_o=file_o,
                        file_c=file_c,
                        file_o_value=_data_o,
                    ),
                )

    @print_decorator()
    def _ddiff(
        self,
        file_o: str,
        file_c: str,
        data_o: Any,
        data_c: Any,
        path: str = "",
        depth: int = 0,
    ) -> None:
        if isinstance(data_o, OrderedDict):
            same = self._compare_types(
                path=path,
                file_o=file_o,
                file_c=file_c,
                data_o=data_o,
                data_c=data_c,
                depth=depth,
            )
            if not same:
                return
            self._compare_dict(
                path=path,
                file_o=file_o,
                file_c=file_c,
                data_o=data_o,
                data_c=data_c,
                depth=depth,
            )
        else:
            same = self._compare_types(
                path=path,
                file_o=file_o,
                file_c=file_c,
                data_o=data_o,
                data_c=data_c,
                depth=depth,
            )
            if not same:
                return
            else:
                if isinstance(data_o, List) and isinstance(data_c, List):
                    if data_o != data_c:
                        same = self._compare_array_sequence(
                            path=path,
                            file_o=file_o,
                            file_c=file_c,
                            data_o=data_o,
                            data_c=data_c,
                            depth=depth,
                        )
                        if not same:
                            return
                        same = self._compare_values(
                            path=path,
                            file_o=file_o,
                            file_c=file_c,
                            data_o=data_o,
                            data_c=data_c,
                            depth=depth,
                        )
                        if not same:
                            return
                same = self._compare_values(
                    path=path,
                    file_o=file_o,
                    file_c=file_c,
                    data_o=data_o,
                    data_c=data_c,
                    depth=depth,
                )
                if not same:
                    return

    @print_decorator()
    def ddiff(self):
        self._ddiff(
            file_o=self.file_o,
            file_c=self.file_c,
            data_o=self.data_o,
            data_c=self.data_c,
            path="",
            depth=0,
        )
        self._ddiff(
            file_o=self.file_c,
            file_c=self.file_o,
            data_o=self.data_c,
            data_c=self.data_o,
            path="",
            depth=0,
        )
