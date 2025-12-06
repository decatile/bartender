class InvalidSpecifierException(Exception):
    def __init__(self, lineno: int, value: str):
        super().__init__(f"unable to parse specifier '{value}' at line {lineno}")


class MalformedSpecifiersException(ExceptionGroup):
    def __init__(self, filepath: str, errors: list[InvalidSpecifierException]):
        super().__init__(f'Malformed specifiers in file {filepath}', errors)
