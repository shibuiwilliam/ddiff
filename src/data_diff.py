from typing import Tuple, List, Any
from collections import OrderedDict, Counter
from enum import Enum


def format_print(*args):
    for a in args:
        print(a)
    print("----------")


class DIFFERENCE(Enum):
    DIFFERENT_TYPES = "different types"
    DIFFERENT_VALUES = "different values"
    ARRAY_IN_DIFFERENT_SEQUENCE = "array in different sequence"
    KEY_NOT_IN_FILE_0 = "key not in file_0"
    KEY_NOT_IN_FILE_1 = "key not in file_1"


class DifferentTypes(object):
    def __init__(self, path: str, file_0_value: Any, file_1_value: Any, file_0_type: str, file_1_type: str):
        self.path = path
        self.file_0_value = file_0_value
        self.file_1_value = file_1_value
        self.file_0_type = file_0_type
        self.file_1_type = file_1_type
        self.status = DIFFERENCE.DIFFERENT_TYPES


class DifferentValues(object):
    def __init__(self, path: str, file_0_value: Any, file_1_value: Any):
        self.path = path
        self.file_0_value = file_0_value
        self.file_1_value = file_1_value
        self.status = DIFFERENCE.DIFFERENT_VALUES


class ArrayInDifferentSequence(object):
    def __init__(self, path: str, file_0_array: List[Any], file_1_array: List[Any]):
        self.path = path
        self.file_0_array = file_0_array
        self.file_1_array = file_1_array
        self.status = DIFFERENCE.ARRAY_IN_DIFFERENT_SEQUENCE


class KeyNotInFile0(object):
    def __init__(self, path: str, file_1_value: Any):
        self.path = path
        self.file_1_value = file_1_value
        self.status = DIFFERENCE.KEY_NOT_IN_FILE_0


class KeyNotInFile1(object):
    def __init__(self, path: str, file_0_value: Any):
        self.path = path
        self.file_0_value = file_0_value
        self.status = DIFFERENCE.KEY_NOT_IN_FILE_0


def data_diff(
    file_data_0: Tuple[str, OrderedDict],
    file_data_1: Tuple[str, OrderedDict],
    path: str = "",
):

    file_0 = file_data_0[0]
    data_0 = file_data_0[1]
    file_1 = file_data_1[0]
    data_1 = file_data_1[1]

    diffs = OrderedDict()

    queue = [{"path": path, "key": ".", "value": data_0}]

    while len(queue) > 0:
        _data = queue.pop()
        _data_0 = _data["value"]
        _path_0 = _data["path"]
        for key, _data_0_value in _data_0.items():
            path = f"{_path_0}.{key}"
            paths = path.split(".")[1:]
            _data_1_value = data_1
            for p in paths:
                if p in _data_1_value.keys():
                    _data_1_value = _data_1_value[p]
                else:
                    diffs[path] = KeyNotInFile1(path=path, file_0_value=_data_0_value)
            if type(_data_0_value) != type(_data_1_value):
                diffs[path] = DifferentTypes(
                    path=path,
                    file_0_value=_data_0_value,
                    file_1_value=_data_1_value,
                    file_0_type=type(_data_0_value).__name__,
                    file_1_type=type(_data_1_value).__name__,
                )
            if isinstance(_data_0_value, OrderedDict):
                queue.append({"path": path, "key": key, "value": _data_0_value})
            else:
                if isinstance(_data_0_value, List):
                    if not isinstance(_data_1_value, List):
                        diffs[path] = DifferentValues(path, file_0_value=_data_0_value, file_1_value=_data_1_value)
                    c_0 = Counter(_data_0_value)
                    c_1 = Counter(_data_1_value)
                    if c_0 == c_1:
                        if _data_0_value != _data_1_value:
                            diffs[path] = ArrayInDifferentSequence(
                                path=path, file_0_array=_data_0_value, file_1_array=_data_1_value
                            )
                    else:
                        diffs[path] = DifferentValues(path=path, file_0_value=_data_0_value, file_1_value=_data_1_value)
                else:
                    if _data_0_value != _data_1_value:
                        diffs[path] = DifferentValues(path=path, file_0_value=_data_0_value, file_1_value=_data_1_value)
    print(diffs)