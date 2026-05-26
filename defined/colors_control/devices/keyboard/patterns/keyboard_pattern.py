from colors_control.objects.color import Color
from colors_control.objects.color_pattern import ColorPattern

from ..objects import KeyboardColor

class KeyboardPattern(ColorPattern[KeyboardColor]):
    def __init__(self, *colors: KeyboardColor) -> None:
        super().__init__(*colors)

    def __str__(self) -> str:
        return ",".join([str(i) for i in self.get_colors()])

