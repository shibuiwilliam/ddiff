from collections import Counter, OrderedDict
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union


class DIFFERENCE(Enum):
    DIFFERENT_TYPES = "different types"
    DIFFERENT_VALUES = "different values"
    ARRAY_IN_DIFFERENT_SEQUENCE = "array in different sequence"
    KEY_NOT_IN_FILE_0 = "key not in file_0"
    KEY_NOT_IN_FILE_1 = "key not in file_1"


class AbstractDifference(object):
    def __init__(self, path: str, file_0: str, file_1: str):
        self.path: str = path
        self.file_0: str = file_0
        self.file_1: str = file_1
        self.status: DIFFERENCE


class DifferentTypes(AbstractDifference):
    def __init__(
        self,
        path: str,
        file_0: str,
        file_1: str,
        file_0_value: Any,
        file_1_value: Any,
        file_0_type: str,
        file_1_type: str,
    ):
        super().__init__(path=path, file_0=file_0, file_1=file_1)
        self.file_0_value: Any = file_0_value
        self.file_1_value: Any = file_1_value
        self.file_0_type: str = file_0_type
        self.file_1_type: str = file_1_type
        self.status: DIFFERENCE = DIFFERENCE.DIFFERENT_TYPES


class DifferentValues(AbstractDifference):
    def __init__(self, path: str, file_0: str, file_1: str, file_0_value: Any, file_1_value: Any):
        super().__init__(path=path, file_0=file_0, file_1=file_1)
        self.file_0_value: Any = file_0_value
        self.file_1_value: Any = file_1_value
        self.status: DIFFERENCE = DIFFERENCE.DIFFERENT_VALUES


class ArrayInDifferentSequence(AbstractDifference):
    def __init__(self, path: str, file_0: str, file_1: str, file_0_array: List[Any], file_1_array: List[Any]):
        super().__init__(path=path, file_0=file_0, file_1=file_1)
        self.file_0_array: List = file_0_array
        self.file_1_array: List = file_1_array
        self.status: DIFFERENCE = DIFFERENCE.ARRAY_IN_DIFFERENT_SEQUENCE


class KeyNotInFile0(AbstractDifference):
    def __init__(self, path: str, file_0: str, file_1: str, file_1_value: Any):
        super().__init__(path=path, file_0=file_0, file_1=file_1)
        self.file_1_value: Any = file_1_value
        self.status: DIFFERENCE = DIFFERENCE.KEY_NOT_IN_FILE_0


class KeyNotInFile1(AbstractDifference):
    def __init__(self, path: str, file_0: str, file_1: str, file_0_value: Any):
        super().__init__(path=path, file_0=file_0, file_1=file_1)
        self.file_0_value: Any = file_0_value
        self.status: DIFFERENCE = DIFFERENCE.KEY_NOT_IN_FILE_0


class Comparer(object):
    line_separator = "-------"

    def __init__(self, file_0: str, file_1: str, data_0: Any, data_1: Any):
        self.file_0 = file_0
        self.file_1 = file_1
        self.data_0 = data_0
        self.data_1 = data_1
        self.__diffs: OrderedDict[str, AbstractDifference] = OrderedDict()

    def __call__(self):
        self.data_diff()

    @property
    def diffs(self) -> OrderedDict[str, AbstractDifference]:
        return self.__diffs

    def pretty_print(self):
        for k, v in self.diffs.items():
            print(f"{Comparer.line_separator}")

    def data_diff(self):
        self._data_diff(data_o=self.data_0, data_c=self.data_1)

    def _data_diff(self, data_o: Dict, data_c: Dict) -> None:
        path = ""

        queue: List[Dict] = [{"path": path, "key": ".", "value": data_o}]

        while len(queue) > 0:
            _data = queue.pop()
            _data_o: Dict = _data["value"]
            _path_o = _data["path"]
            for key, _data_o_value in _data_o.items():
                _path = f"{_path_o}.{key}"
                _paths = _path.split(".")[1:]
                _data_c: Union[Dict, str] = data_c
                for p in _paths:
                    if p in _data_c.keys():
                        _data_c = _data_c[p]
                    else:
                        if _path not in self.__diffs.keys():
                            self.__diffs[_path] = KeyNotInFile1(path=_path, file_0=self.file_0, file_1=self.file_1, file_0_value=_data_o_value)
                if type(_data_o_value) != type(_data_c):
                    self.__diffs[path] = DifferentTypes(
                        path=path,
                        file_0=self.file_0,
                        file_1=self.file_1,
                        file_0_value=_data_o_value,
                        file_1_value=_data_c,
                        file_0_type=type(_data_o_value).__name__,
                        file_1_type=type(_data_c).__name__,
                    )
                    break
                if isinstance(_data_o_value, OrderedDict):
                    queue.append({"path": path, "key": key, "value": _data_o_value})
                    break
                if isinstance(_data_o_value, List):
                    c_0 = Counter(_data_o_value)
                    c_1 = Counter(_data_c)
                    if _data_o_value != _data_c:
                        if c_0 == c_1:
                            self.__diffs[path] = ArrayInDifferentSequence(
                                path=path,
                                file_0=self.file_0,
                                file_1=self.file_1,
                                file_0_array=_data_o_value,
                                file_1_array=_data_c,
                            )
                            break
                        else:
                            self.__diffs[path] = DifferentValues(
                                path=path,
                                file_0=self.file_0,
                                file_1=self.file_1,
                                file_0_value=_data_o_value,
                                file_1_value=_data_c,
                            )
                            break
                if _data_o_value != _data_c:
                    self.__diffs[path] = DifferentValues(
                        path=path,
                        file_0=self.file_0,
                        file_1=self.file_1,
                        file_0_value=_data_o_value,
                        file_1_value=_data_c,
                    )
                    break
