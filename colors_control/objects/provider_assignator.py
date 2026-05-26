from .device import ColoredDevice

class DeviceProviderAssignator():
    def __init__(self, name: str) -> None:
        self._name = name

    def get_name(self) -> str:
        return self._name
    
    def get_assigned_provider_for_device(self, device: ColoredDevice) -> str | None:
        raise NotImplementedError("not implemented for " + repr(self))
    
    def accepts(self, device: ColoredDevice) -> bool:
        raise NotImplementedError("not implemented for " + repr(self))
    
