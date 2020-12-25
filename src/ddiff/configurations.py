class Configurations:
    line_separator: str = "-------"
    indent_size: int = 4
    debug: bool = False

    @classmethod
    def indent(cls) -> str:
        return " " * cls.indent_size
