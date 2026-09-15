from bartender.interactor.abc import AbstractInteractor
from bartender.interactor.spec import PackageSpec
from bartender.log import L


class SimpleInteractor(AbstractInteractor):
    def __init__(self, filepath: str):
        self._filepath = filepath

    def load_specs(self) -> list[PackageSpec]:
        L.info(f'Simple interactor does not load specs')
        return []

    def save_specs(self, specs: list[PackageSpec]) -> None:
        L.info(f'Simple interactor does not write to {self._filepath}')

    def dump_specs(self, specs: list[PackageSpec]) -> str:
        return 'Simple interactor does not dump specs'


__all__ = ('SimpleInteractor',)
