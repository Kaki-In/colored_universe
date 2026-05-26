from .color_pattern import ColorPattern

import abc as _abc

class ColoredDevice(_abc.ABC):
    def __init__(self, typename: str, name: str, default_color: ColorPattern) -> None:
        self.__device_name = typename + ":" + name
        self.__device_color = default_color

        self.apply()
    
    def on_integrated(self) -> None:
        pass

    def on_expulsed(self) -> None:
        pass

    @property
    @_abc.abstractmethod
    def assignator_name(self) -> str | None:
        ...

    @property
    def device_name(self) -> str:
        return self.__device_name
    
    @property
    def pattern(self) -> ColorPattern:
        return self.__device_color
    
    def set_pattern(self, color: ColorPattern) -> None:
        self.__device_color = color
        self.apply()

    @_abc.abstractmethod
    def apply(self) -> None:
        ...

