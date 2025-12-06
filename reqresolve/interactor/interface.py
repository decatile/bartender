from abc import ABC, abstractmethod

from reqresolve.package_spec import PackageSpec


class AbstractInteractor(ABC):
    @abstractmethod
    def load_specs(self) -> list[PackageSpec]: ...

    @abstractmethod
    def save_specs(self, specs: list[PackageSpec]): ...
