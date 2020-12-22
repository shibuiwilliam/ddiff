from typing import Tuple
from collections import OrderedDict, Counter


def format_print(*args):
    for a in args:
        print(a)
    print("----------")


def data_diff(
    file_data_0: Tuple[str, OrderedDict],
    file_data_1: Tuple[str, OrderedDict],
    path: str = "",
):
    file_0 = file_data_0[0]
    data_0 = file_data_0[1]
    file_1 = file_data_1[0]
    data_1 = file_data_1[1]
    original_path = path
    for key, value in data_0.items():
        path = f"{original_path}.{key}"
        if isinstance(value, OrderedDict):
            if key not in data_1.keys():
                format_print(f"{file_0} + {path}", f"{file_1} - {path}")
            else:
                data_diff((file_0, data_0[key]), (file_1, data_1[key]), path)
        elif isinstance(value, list):
            if key not in data_1.keys():
                format_print(f"{file_0} + {path}", f"{file_1} - {path}")
            else:
                if isinstance(data_1[key], list):
                    counted_0 = Counter(value)
                    counted_1 = Counter(data_1[key])
                    if counted_0 != counted_1:
                        format_print(
                            f"{path}:",
                            f"\t{file_0}: {data_0[key]}",
                            f"\t{file_1}: {data_1[key]}",
                        )
        else:
            if key not in data_1.keys():
                format_print(f"{file_0} + {path}", f"{file_1} - {path}")
            else:
                if data_0[key] != data_1[key]:
                    format_print(
                        f"{path}:",
                        f"\t{file_0}: {data_0[key]}",
                        f"\t{file_1}: {data_1[key]}",
                    )
