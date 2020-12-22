from collections import OrderedDict
import click

from src.file_controller import FileController
from src.data_diff import data_diff


@click.command()
@click.argument("files", nargs=2)
def main(files: str):
    file_controller = FileController(file_0=files[0], file_1=files[1])

    data_diff(
        file_data_0=(files[0], file_controller.data_0),
        file_data_1=(files[1], file_controller.data_1),
        path="",
    )


if __name__ == "__main__":
    main()
