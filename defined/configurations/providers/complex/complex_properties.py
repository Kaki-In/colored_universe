import configuration as _configuration
import typing as _T

from .complex_properties_object import ComplexPropertiesObject, ComplexKeyboardPatternObject

from defined.colors_control.devices.keyboard.objects import KeyboardColor
from defined.colors_control.devices.keyboard.patterns import *

class ComplexColorProviderProperties(_configuration.SettingsFile[ComplexPropertiesObject]):
    def __init__(self, path: str) -> None:
        super().__init__(path, {
            'pattern': {
                'left': {
                    'name': 'red',
                    'red': 255,
                    'green': 0,
                    'blue': 0
                },
                'middle': {
                    'name': 'red',
                    'red': 255,
                    'green': 0,
                    'blue': 0
                },
                'right': {
                    'name': 'red',
                    'red': 255,
                    'green': 0,
                    'blue': 0
                },
                'logo': None,
                'front_left': None,
                'front_right': None,
                'mouse': None
            },
            'transition_duration_time': 1000
        })

    def _get_pattern_from_object(self, pattern: ComplexKeyboardPatternObject) -> ComplexKeyboardColorPattern:
        colors: dict[str, _T.Optional[KeyboardColor]] = {}

        for name in ('right', 'logo', 'front_left', 'front_right', 'mouse'):
            color = pattern[name]

            if color is None:
                colors["color_" + name] = None
            else:
                colors["color_" + name] = KeyboardColor(**color)

        return ComplexKeyboardColorPattern(
            KeyboardColor(**pattern['left']),
            KeyboardColor(**pattern['middle']),
            **colors
        )
        
    def _get_pattern_object(self, pattern: ComplexKeyboardColorPattern) -> ComplexKeyboardPatternObject:
        colors: ComplexKeyboardPatternObject = {} #type:ignore

        color_names = ('left', 'middle', 'right', 'logo', 'front_left', 'front_right', 'mouse')

        for color_index in range(len(color_names)):
            color = pattern.get_colors()[color_index]
            colors[color_names[color_index]] = {
                'name': color.get_name(),
                'red': color.get_red(),
                'green': color.get_green(),
                'blue': color.get_blue()
            }

        return colors
        
    def get_pattern(self) -> ComplexKeyboardColorPattern:
        return self._get_pattern_from_object(self.get_content()['pattern'])

    def get_transition_duration_time(self) -> int:
        return self.get_content()['transition_duration_time']


