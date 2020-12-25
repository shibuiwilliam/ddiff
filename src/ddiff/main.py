from collections import OrderedDict

import click

from ddiff.configurations import OUTPUT_FORMAT, Configurations
from ddiff.data_diff import Ddiff
from ddiff.file_controller import FileController


@click.command()
@click.argument(
    "files",
    nargs=2,
    required=True,
    type=str,
)
@click.option(
    "--steps",
    "-s",
    type=bool,
    default=False,
    help="print results in steps",
)
@click.option(
    "--indent_size",
    "-i",
    type=int,
    default=4,
    help="indentation size",
)
@click.option(
    "--line_separator",
    "-l",
    type=str,
    default="-------",
    help="line separator",
)
@click.option(
    "--output_filepath",
    "-o",
    type=str,
    default="",
    help="output file path",
)
@click.option(
    "--output_format",
    "-f",
    type=click.Choice(["default", "json", "yaml"]),
    default="default",
    help="output format",
)
@click.option(
    "--debug",
    "-d",
    type=bool,
    default=False,
    help="run in debug mode",
)
def main(
    files: str,
    steps: bool,
    indent_size: int,
    line_separator: str,
    output_filepath: str,
    output_format: str,
    debug: bool,
):
    Configurations.indent_size = indent_size
    Configurations.line_separator = line_separator
    Configurations.debug = debug
    file_controller = FileController(file_o=files[0], file_c=files[1])

    file_o = file_controller.file_o
    file_c = file_controller.file_c
    data_o = file_controller.data_o
    data_c = file_controller.data_c

    if output_format == OUTPUT_FORMAT.DEFAULT.value:
        _output_format = OUTPUT_FORMAT.DEFAULT
    elif output_format == OUTPUT_FORMAT.JSON.value:
        _output_format = OUTPUT_FORMAT.JSON
    elif output_format == OUTPUT_FORMAT.YAML.value:
        _output_format = OUTPUT_FORMAT.YAML
    else:
        _output_format = OUTPUT_FORMAT.DEFAULT

    ddiff = Ddiff(
        file_o=file_o,
        file_c=file_c,
        data_o=data_o,
        data_c=data_c,
        output_format=_output_format,
        indent_key=steps,
    )
    ddiff()
    ddiff.pretty_print()


if __name__ == "__main__":
    main()
