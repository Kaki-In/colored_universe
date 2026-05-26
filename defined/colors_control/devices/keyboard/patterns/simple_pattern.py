from .keyboard_pattern import KeyboardPattern

from ..objects import KeyboardColor

class SimpleKeyboardColorPattern(KeyboardPattern):
    def __init__(self, color: KeyboardColor) -> None:
        super().__init__(color)

    def get_color(self) -> KeyboardColor:
        return self._colors[0]


