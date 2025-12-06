import rich

from .interface import AbstractInteractor
from .requirements import RequirementsInteractor


def for_filepath(filepath: str) -> AbstractInteractor:
    if filepath.endswith('.txt'):
        rich.print('[green]Detected plaintext (requirements.txt) file')
        return RequirementsInteractor(filepath)
    else:
        raise NotImplementedError('Only plaintext supported yet.')
