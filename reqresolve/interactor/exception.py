class InvalidSpecifierException(Exception):
    def __init__(self, value: str, lineno: int | None = None):
        if lineno is not None:
            super().__init__(f"unable to parse specifier '{value}' at line {lineno}")
        else:
            super().__init__(f"unable to parse specifier '{value}'")


class MalformedSpecifiersException(ExceptionGroup):
    def __init__(self, filepath: str, errors: list[InvalidSpecifierException]):
        super().__init__(f'Malformed specifiers in file {filepath}', errors)


class UnsupportedOperationException(Exception): ...
