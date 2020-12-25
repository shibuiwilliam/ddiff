import random
import string
import uuid
from abc import ABCMeta, abstractmethod
from collections import Counter, OrderedDict
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from ddiff.configurations import Configurations


def print_decorator() -> Callable:
    def _print_decorator(func) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            if Configurations.debug:
                job_id = str(uuid.uuid4())[:6]
                print(f"START {job_id}\n\tfunc:\t{func.__name__}\n\targs:\t{args}\n\tkwargs:\t{kwargs}")
                res = func(*args, **kwargs)
                print(f"RETURN FROM {job_id}\n\treturn:\t{res}")
                return res
            else:
                res = func(*args, **kwargs)
                return res

        return wrapper

    return _print_decorator


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


class Comparer(object):
    def __init__(
        self,
        file_o: str,
        file_c: str,
        data_o: Any,
        data_c: Any,
        indent_key: bool = False,
    ):
        self.file_o = file_o
        self.file_c = file_c
        self.data_o = data_o
        self.data_c = data_c
        self.indent_key = indent_key

        self.__diffs: OrderedDict[str, AbstractDifference] = OrderedDict()

        self.separator = self.random_separator()

    def __call__(self):
        self.data_diff()

    @property
    def diffs(self) -> OrderedDict:
        return self.__diffs

    @print_decorator()
    def add_diff(self, path: str, diff: AbstractDifference):
        if path not in self.__diffs.keys():
            self.__diffs[path] = diff

    @print_decorator()
    def random_separator(self, n=32) -> str:
        if Configurations.debug:
            return "."
        _sep = "".join(random.choices(string.ascii_letters + string.digits, k=n))
        return f"<{_sep}>"

    @print_decorator()
    def pretty_print(self):
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
                self._data_diff(
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
    def _data_diff(
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
                        else:
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
    def data_diff(self):
        self._data_diff(
            file_o=self.file_o,
            file_c=self.file_c,
            data_o=self.data_o,
            data_c=self.data_c,
            path="",
            depth=0,
        )
        self._data_diff(
            file_o=self.file_c,
            file_c=self.file_o,
            data_o=self.data_c,
            data_c=self.data_o,
            path="",
            depth=0,
        )
