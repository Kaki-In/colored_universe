from colors_control.objects.device import ColoredDevice

from ..objects.keyboardcolor import KEYBOARD_COLOR_NONE
from ..enums.brightnessidentifier import KeyboardBrightnessIdentifier
from ..enums.modeidentifier import KeyboardModeIdentifier

from ..objects.brightness import KeyboardBrightness
from ..objects.mode import KeyboardMode

from ..patterns.keyboard_pattern import KeyboardPattern
from ..patterns.simple_pattern import SimpleKeyboardColorPattern

from defined.configurations.devices import LocalColorKeyboardConfiguration

import os as _os
import termcolor as _termcolor
import random as _random

class LocalColorKeyboard(ColoredDevice[KeyboardPattern]):
    def __init__(self, 
            name: str,
            configuration: LocalColorKeyboardConfiguration,
            initial_pattern: KeyboardPattern = SimpleKeyboardColorPattern(KEYBOARD_COLOR_NONE), 
            brightness: KeyboardBrightness = KeyboardBrightness(KeyboardBrightnessIdentifier.RGB), 
            mode: KeyboardMode = KeyboardMode(KeyboardModeIdentifier.NORMAL),
        ) -> None:
        self._brightness = brightness
        self._mode = mode

        self._configuration = configuration
        self._last_pattern = initial_pattern

        super().__init__("keyboard", name, initial_pattern)

    def get_configuration(self) -> LocalColorKeyboardConfiguration:
        return self._configuration
    
    def get_assignator_name(self) -> str | None:
        return self._configuration.get_configuration().get_assigned_provider()
    
    def apply(self) -> None:
        pattern = self.get_pattern()

        if str(pattern) == str(self._last_pattern):
            return
        
        self._last_pattern = pattern

        print('\b\r', end='')
        for color in pattern.get_colors():
            print(_termcolor.colored("0", force_color=True, color=(color.get_red(), color.get_green(), color.get_blue())).replace("\x1b[0m", ''), end='')
        
        print(_random.random())

        _os.system("msiklm {pattern} {brightness} {mode}".format(pattern = str(self.get_pattern()), brightness = str(self._brightness), mode = str(self._mode)))
    
    def get_brigthness(self) -> KeyboardBrightness:
        return self._brightness
    
    def get_mode(self) -> KeyboardMode:
        return self._mode
    
    def set_brigthness(self, brightness: KeyboardBrightness) -> None:
        self._brightness = brightness
        self.apply()
    
    def set_mode(self, mode: KeyboardMode) -> None:
        self._mode = mode
        self.apply()
    
 