from .device import ColoredDevice

import abc as _abc

class DeviceProviderAssignator(_abc.ABC):
    def __init__(self, name: str) -> None:
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name
    
    @_abc.abstractmethod
    def get_assigned_provider_for_device(self, device: ColoredDevice) -> str | None:
        ...
    
    @_abc.abstractmethod
    def accepts(self, device: ColoredDevice) -> bool:
        ...
    
