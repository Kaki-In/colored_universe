from colors_control.objects.color import Color

from .keyboard_pattern import KeyboardPattern

from ..objects.keyboardcolor import *

import typing as _T

class ComplexKeyboardColorPattern(KeyboardPattern):
    def __init__(self,
                 color_left: KeyboardColor,
                 color_middle: KeyboardColor,
                 color_right: _T.Optional[KeyboardColor] = None,
                 color_logo: _T.Optional[KeyboardColor] = None,
                 color_front_left: _T.Optional[KeyboardColor] = None,
                 color_front_right: _T.Optional[KeyboardColor] = None,
                 color_mouse: _T.Optional[KeyboardColor] = None,
                ) -> None:
        
        colors = [
            color_left,
            color_middle,
            color_right,
            color_logo,
            color_front_left,
            color_front_right,
            color_mouse
        ]

        found_colors = []

        for color in colors:
            if color is None:
                color = KEYBOARD_COLOR_NONE

            found_colors.append(color)

        super().__init__(*found_colors)

    def get_color_left(self) -> KeyboardColor:
        return self.get_colors()[0]

    def get_color_middle(self) -> KeyboardColor:
        return self.get_colors()[1]

    def get_color_right(self) -> KeyboardColor:
        return self.get_colors()[2]

    def get_color_logo(self) -> KeyboardColor:
        return self.get_colors()[3]

    def get_color_front_left(self) -> KeyboardColor:
        return self.get_colors()[4]

    def get_color_front_right(self) -> KeyboardColor:
        return self.get_colors()[5]

    def get_color_mouse(self) -> KeyboardColor:
        return self.get_colors()[6]

        
