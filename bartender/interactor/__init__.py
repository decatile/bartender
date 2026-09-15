from ..log import L
from .abc import AbstractInteractor
from .exception import (
    InvalidSpecifierException,
    MalformedSpecifiersException,
    UnsupportedOperationException,
)
from .pyproject import PyprojectInteractor
from .requirements import RequirementsInteractor


def for_filepath(filepath: str) -> AbstractInteractor:
    if filepath.endswith(".txt"):
        L.info("Detected plaintext (requirements.txt) file")
        return RequirementsInteractor(filepath)
    elif filepath.endswith(".toml"):
        L.info("Detected toml (pyproject.toml) file")
        return PyprojectInteractor(filepath)
    else:
        raise ValueError("Invalid file extension (.txt or .toml expected)")


__all__ = (
    "InvalidSpecifierException",
    "MalformedSpecifiersException",
    "UnsupportedOperationException",
    "for_filepath",
)
