import typing as _T

from .device_scanner import *
from .provider_scanner import *
from .provider_assignator import *

class Plugin():
    def __init__(self,
                 hash:str,
                 name:str,
                 pathname: str,
                 devices_scanners: list[DevicesScanner],
                 providers_scanners: list[ProvidersScanner],
                 assignators: list[DeviceProviderAssignator],
                 dependencies: list[str],
                 namespace: dict[str, dict]) -> None:

        self._name = name

        self._path = pathname

        self._device_scanners = devices_scanners
        self._providers_scanners = providers_scanners
        self._assignators = assignators

        self._dependencies = dependencies
        self._namespace = namespace

        self._sha256 = hash

    def get_name(self) -> str:
        return self._name
    
    def get_pathname(self) -> str:
        return self._path
    
    def get_hash(self) -> str:
        return self._sha256
    
    def get_dependencies(self) -> list[str]:
        return self._dependencies
    
    def get_namespace(self) -> dict[str, dict]:
        return self._namespace

    def get_devices_scanners(self) -> _T.Sequence[DevicesScanner]:
        return self._device_scanners

    def get_providers_scanners(self) -> _T.Sequence[ProvidersScanner]:
        return self._providers_scanners

    def get_assignators(self) -> _T.Sequence[DeviceProviderAssignator]:
        return self._assignators

