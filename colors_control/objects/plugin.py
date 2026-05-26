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

        self.__name = name

        self.__path = pathname

        self.__device_scanners = devices_scanners
        self.__providers_scanners = providers_scanners
        self.__assignators = assignators

        self.__dependencies = dependencies
        self.__namespace = namespace

        self.__sha256 = hash

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def pathname(self) -> str:
        return self.__path
    
    @property
    def hash(self) -> str:
        return self.__sha256
    
    @property
    def dependencies(self) -> list[str]:
        return self.__dependencies
    
    @property
    def namespace(self) -> dict[str, dict]:
        return self.__namespace

    @property
    def devices_scanners(self) -> _T.Sequence[DevicesScanner]:
        return self.__device_scanners

    @property
    def providers_scanners(self) -> _T.Sequence[ProvidersScanner]:
        return self.__providers_scanners

    @property
    def assignators(self) -> _T.Sequence[DeviceProviderAssignator]:
        return self.__assignators

