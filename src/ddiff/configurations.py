from enum import Enum


class Configurations:
    line_separator: str = "-------"
    indent_size: int = 4
    debug: bool = False

    @classmethod
    def indent(cls) -> str:
        return " " * cls.indent_size


class OUTPUT_FORMAT(Enum):
    DEFAULT = "default"
    JSON = "json"
    YAML = "yaml"
