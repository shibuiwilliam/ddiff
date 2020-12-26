from collections import OrderedDict
from typing import Union

import click

from ddiff.configurations import OUTPUT_FORMAT, Configurations
from ddiff.data_diff import Ddiff
from ddiff.file_controller import FileLoader, export_to_json, export_to_yaml


@click.command(name="ddiff")
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
    file_loader = FileLoader(file_o=files[0], file_c=files[1])

    file_o = file_loader.file_o
    file_c = file_loader.file_c
    data_o = file_loader.data_o
    data_c = file_loader.data_c

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

    if output_filepath:
        if _output_format == OUTPUT_FORMAT.DEFAULT:
            raise ValueError("output_format must be yaml or json to export diffs to a file")
        odict_diff = ddiff.diffs_to_dict()
        dict_diff = dict(odict_diff)
        if _output_format == OUTPUT_FORMAT.JSON:
            export_to_json(output_filepath=output_filepath, dict_diff=dict_diff)
        if _output_format == OUTPUT_FORMAT.YAML:
            export_to_yaml(output_filepath=output_filepath, dict_diff=dict_diff)


if __name__ == "__main__":
    main()
