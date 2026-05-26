from .device import ColoredDevice
import typing as _T

class ColorProvider:
    def __init__(self, type:str, name: str):
        self._name = type + ((":" + name) if name else "")

    def on_start(self) -> None:
        print("start providing color " + self._name)

    def on_terminate(self) -> None:
        print("finished providing color " + self._name)

    def get_name(self) -> str:
        return self._name

    def can_handle(self, device: ColoredDevice) -> bool:
        raise NotImplementedError("not implemented for " + repr(self))
    
    def apply_pattern(self, devices: _T.Sequence[ColoredDevice]) -> None:
        raise NotImplementedError("not implemented for " + repr(self))
    
