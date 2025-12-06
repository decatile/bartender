import os

from reqresolve.interactor.interface import AbstractInteractor
from reqresolve.package_spec import PackageSpec


class RequirementsInteractor(AbstractInteractor):
    def __init__(self, filepath: str):
        self._filepath = filepath

    def load_specs(self) -> list[PackageSpec]:
        result: list[PackageSpec] = []
        errors: list[Exception] = []

        with open(self._filepath) as f:
            for lineno, line in enumerate(f, 1):
                try:
                    result.append(PackageSpec.parse(line))
                except ValueError:
                    errors.append(Exception(f"Invalid specifier at line {lineno}: '{line.strip()}'"))

        if errors:
            raise ExceptionGroup(f'Malformed specifiers in {self._filepath}', errors)

        return result

    def save_specs(self, specs: list[PackageSpec]):
        os.rename(self._filepath, self._filepath + '.bak')

        with open(self._filepath, 'w+') as f:
            for spec in specs:
                f.write(str(spec))
                f.write('\n')
