from ruamel.yaml import YAML, add_constructor, resolver
from collections import OrderedDict
import click


@click.command()
@click.argument("file", nargs=1)
@click.option("-f", "--file", "file", required=True, type=str, help="file path")
def main(file: str):
    add_constructor(
        resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        lambda loader, node: OrderedDict(loader.construct_pairs(node)),
    )

    yaml = YAML()
    yaml.default_flow_style = False

    with open(file, "r", encoding="utf-8") as f:
        data = yaml.load(f)

    with open("/tmp/output.yaml", "w", encoding="utf-8") as f:
        yaml.dump(data, f)


if __name__ == "__main__":
    main()
