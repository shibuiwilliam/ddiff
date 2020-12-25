from collections import OrderedDict

import click

from src.data_diff import Comparer
from src.file_controller import FileController
from src.configurations import Configurations


@click.command()
@click.argument("files", nargs=2, required=True, type=str)
@click.option("--steps", "-s", type=bool, default=False, help="print in steps")
@click.option("--indent_size", "-i", type=int, default=4, help="indent size")
@click.option("--line_separator", "-l", type=str, default="-------", help="line separator")
@click.option("--debug", "-d", type=bool, default=False, help="debug mode")
def main(files: str, steps: bool, indent_size: int, line_separator: str, debug: bool):
    Configurations.indent_size = indent_size
    Configurations.line_separator = line_separator
    Configurations.debug = debug
    file_controller = FileController(file_o=files[0], file_c=files[1])

    file_o = file_controller.file_o
    file_c = file_controller.file_c
    data_o = file_controller.data_o
    data_c = file_controller.data_c

    comparer = Comparer(
        file_o=file_o,
        file_c=file_c,
        data_o=data_o,
        data_c=data_c,
        indent_key=steps,
    )
    comparer()
    comparer.pretty_print()


if __name__ == "__main__":
    main()
