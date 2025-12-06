from .interface import AbstractInteractor
from .requirements import RequirementsInteractor


def for_filepath(filepath: str) -> AbstractInteractor:
    if filepath.endswith('.txt'):
        return RequirementsInteractor(filepath)
    else:
        raise NotImplementedError
