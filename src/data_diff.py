from typing import Tuple
from collections import OrderedDict, Counter


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
                print(f"{file_0} + {path}")
                print(f"{file_1} - {path}")
                print("-------------")
            else:
                data_diff((file_0, data_0[key]), (file_1, data_1[key]), path)
        elif isinstance(value, list):
            if key not in data_1.keys():
                print(f"{file_0} + {path}")
                print(f"{file_1} - {path}")
                print("-------------")
            else:
                if isinstance(data_1[key], list):
                    counted_0 = Counter(value)
                    counted_1 = Counter(data_1[key])
                    if counted_0 != counted_1:
                        print(f"{path}:")
                        print(f"\t{file_0}: {data_0[key]}")
                        print(f"\t{file_1}: {data_1[key]}")
                        print("-------------")
        else:
            if key not in data_1.keys():
                print(f"{file_0} + {path}")
                print(f"{file_1} - {path}")
                print("-------------")
            else:
                if data_0[key] != data_1[key]:
                    print(f"{path}:")
                    print(f"\t{file_0}: {data_0[key]}")
                    print(f"\t{file_1}: {data_1[key]}")
                    print("-------------")
