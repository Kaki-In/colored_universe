from .device import ColoredDevice
import typing as _T
import abc as _abc

class ColorProvider(_abc.ABC):
    def __init__(self, type:str, name: str):
        self.__name = type + ((":" + name) if name else "")

    def on_start(self) -> None:
        print("start providing color " + self.__name)

    def on_terminate(self) -> None:
        print("finished providing color " + self.__name)

    @property
    def name(self) -> str:
        return self.__name

    @_abc.abstractmethod
    def can_handle(self, device: ColoredDevice) -> bool:
        ...
    
    @_abc.abstractmethod
    def apply_pattern(self, devices: _T.Sequence[ColoredDevice]) -> None:
        ...
    
