import configuration as _configuration

from .simple_properties_object import SimplePropertiesObject

from defined.colors_control.devices.keyboard.objects import KeyboardColor

class SimpleColorProviderProperties(_configuration.SettingsFile[SimplePropertiesObject]):
    def __init__(self, path: str) -> None:
        super().__init__(path, {
            'color': {
                'red': 255,
                'green': 0,
                'blue': 0
            },
            'transition_duration_time': 1000
        })

    def get_color(self) -> KeyboardColor:
        color = self.get_content()['color']

        return KeyboardColor.from_rgb(
            color['red'],
            color['green'],
            color['blue']
        )
    
    def get_transition_duration_time(self) -> int:
        return self.get_content()['transition_duration_time']


