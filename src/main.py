from collections import OrderedDict

import click

from src.data_diff import Comparer
from src.file_controller import FileController


@click.command()
@click.argument("files", nargs=2)
def main(files: str):
    file_controller = FileController(file_0=files[0], file_1=files[1])

    file_0 = file_controller.file_0
    file_1 = file_controller.file_1
    data_0 = file_controller.data_0
    data_1 = file_controller.data_1

    comparer = Comparer(file_0=file_0, file_1=file_1, data_0=data_0, data_1=data_1)
    comparer()
    diffs = comparer()


if __name__ == "__main__":
    main()
