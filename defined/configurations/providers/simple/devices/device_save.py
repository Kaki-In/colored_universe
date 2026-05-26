import configuration as _configuration
import time as _time
import typing as _T

from .device_saves_object import SimpleColorProviderDeviceSavesObject, KeyboardPatternDescription, ComplexKeyboardPatternObject
from defined.colors_control.devices.keyboard.patterns import *
from defined.colors_control.devices.keyboard.objects import KeyboardColor

class SimpleColorProviderDeviceSaves(_configuration.SettingsFile[SimpleColorProviderDeviceSavesObject]):
    def __init__(self, path: str, default_pattern: KeyboardPattern) -> None:
        super().__init__(path, {
            'previous_color': self._get_pattern_object(default_pattern),
            'previous_color_time': _time.monotonic(),
            'previous_target_color': 'none',
        }, "data")

    def _get_pattern_from_object(self, data: KeyboardPatternDescription) -> KeyboardPattern:
        if data['type'] == 'simple':
            return SimpleKeyboardColorPattern(KeyboardColor(**data['pattern']))
        
        elif data['type'] == 'complex':
            pattern = data['pattern']

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
        
        else:
            return SimpleKeyboardColorPattern(KeyboardColor(**data['pattern']))
        
    def _get_pattern_object(self, pattern: KeyboardPattern) -> KeyboardPatternDescription:
        if isinstance(pattern, SimpleKeyboardColorPattern):
            color = pattern.get_color()

            return {
                'type': 'simple',
                'pattern': {
                    'name': color.get_name(),
                    'red': color.get_red(),
                    'green': color.get_green(),
                    'blue': color.get_blue()
                }   
            }
        elif isinstance(pattern, ComplexKeyboardColorPattern):
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

            return {
                'type': 'complex',
                'pattern': colors
            }
        
        else:
            color = pattern.get_colors()[0]

            return {
                'type': 'simple',
                'pattern': {
                    'name': color.get_name(),
                    'red': color.get_red(),
                    'green': color.get_green(),
                    'blue': color.get_blue()
                }   
            }

    def get_previous_color(self) -> KeyboardPattern:
        return self._get_pattern_from_object(
            self.get_content()['previous_color']
        )
        
    def set_previous_color(self, previous_color: KeyboardPattern) -> None:
        content = self.get_content()

        content['previous_color'] = self._get_pattern_object(previous_color)

        self.overwrite(content)
    
    def set_previous_color_with_time(self, pattern: KeyboardPattern, time: float) -> None:
        content  = self.get_content()

        content['previous_color'] = self._get_pattern_object(pattern)

        content['previous_color_time'] = time

        self.overwrite(content)

    def set_new_previous_color_now(self, color: KeyboardPattern) -> None:
        self.set_previous_color_with_time(color, _time.monotonic())

    def get_previous_color_time(self) -> float:
        return self.get_content()['previous_color_time']
    
    def get_previous_color_duration(self) -> float:
        return _time.monotonic() - self.get_previous_color_time()
    
    def set_previous_color_time(self, time: float) -> None:
        content  = self.get_content()

        content['previous_color_time'] = time

        self.overwrite(content)

    def set_previous_color_time_now(self) -> None:
        self.set_previous_color_time(_time.monotonic())

    def get_target_color(self) -> str:
        return self.get_content()['previous_target_color']
    
    def set_target_color(self, color: str) -> None:
        content  = self.get_content()

        content['previous_target_color'] = color

        self.overwrite(content)
    


