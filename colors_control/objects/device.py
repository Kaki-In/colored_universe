from .color_pattern import ColorPattern

import abc as _abc

class ColoredDevice[PatternType: ColorPattern](_abc.ABC):
    def __init__(self, typename: str, name: str, default_color: PatternType) -> None:
        self.__device_name = typename + ":" + name
        self.__device_color = default_color

        self.apply()
    
    @property
    @_abc.abstractmethod
    def zones_count(self) -> int:
        ...
    
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
    def pattern(self) -> PatternType:
        return self.__device_color
    
    @pattern.setter
    def pattern(self, color: PatternType) -> None:
        self.__device_color = color
        self.apply()

    @_abc.abstractmethod
    def apply(self) -> None:
        ...
        
    @_abc.abstractmethod
    def apply_no_pattern(self) -> None:
        ...

