from .color_pattern import ColorPattern

import typing as _T

class ColoredDevice():
    def __init__(self, typename: str, name: str, default_color: ColorPattern) -> None:
        self._device_name = typename + ":" + name
        self._device_color = default_color

        self.apply()
    
    def on_integrated(self) -> None:
        pass

    def on_expulsed(self) -> None:
        pass

    def get_assignator_name(self) -> str | None:
        raise NotImplementedError("not implemented for " + repr(self))

    def get_device_name(self) -> str:
        return self._device_name
    
    def get_pattern(self) -> ColorPattern:
        return self._device_color
    
    def set_pattern(self, color: ColorPattern) -> None:
        self._device_color = color
        self.apply()

    def apply(self) -> None:
        raise NotImplementedError("not implemented for " + repr(self))

