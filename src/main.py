from collections import OrderedDict
import click

from src.file_controller import FileController


@click.command()
@click.argument("files", nargs=2)
def main(files: str):
    file_controller = FileController(file_0=files[0], file_1=files[1])
    print(file_controller.data_0)
    print(file_controller.data_1)


if __name__ == "__main__":
    main()
