import rich

from .abc import AbstractInteractor
from .pyproject import PyprojectInteractor
from .requirements import RequirementsInteractor


def for_filepath(filepath: str) -> AbstractInteractor:
    if filepath.endswith('.txt'):
        rich.print('[green]Detected plaintext (requirements.txt) file')
        return RequirementsInteractor(filepath)
    elif filepath.endswith('.toml'):
        rich.print('[green]Detected toml (pyproject.toml) file')
        return PyprojectInteractor(filepath)
    else:
        raise ValueError('Invalid file extension (.txt or .toml expected)')
