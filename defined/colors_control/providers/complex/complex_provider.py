from colors_control.objects import ColorProvider, ColoredDevice, Color, ProvidersRegister

from defined.colors_control.devices.keyboard.devices import *
from defined.colors_control.devices.keyboard.patterns import *
from defined.colors_control.devices.keyboard.objects import *

from defined.configurations.providers.complex import ComplexConfiguration

import time as _time
import typing as _T

class ComplexColorProvider(ColorProvider):
    def __init__(self, provider_name: str, configuration: ComplexConfiguration) -> None:
        super().__init__("Complex Color", provider_name)
        
        self._configuration = configuration
    
    def get_configuration(self) -> ComplexConfiguration:
        return self._configuration
    
    def can_handle(self, device: ColoredDevice) -> bool:
        return isinstance(device, LocalColorKeyboard)
    
    def get_pattern(self) -> ComplexKeyboardColorPattern:
        return self._configuration.get_properties().get_pattern()
    
    def apply_pattern(self, devices: _T.Sequence[ColoredDevice]) -> None:
        devices_names = [device.get_device_name() for device in devices]

        for device_name in self._configuration.get_saves().get_known_devices():
            if not device_name in devices_names:
                self._configuration.get_saves().forget_device(device_name)

        for device in devices:
            self.apply_pattern_to_device(device)
    
    def get_pattern_id(self, pattern: KeyboardPattern) -> list[str|None]:
        return [color.get_name() for color in pattern.get_colors()]
    
    def apply_pattern_to_device(self, device: ColoredDevice) -> None:
        if type(device) is not LocalColorKeyboard:
            return
        
        device_name = device.get_device_name()
        device_saves = self._configuration.get_saves().get_device_save(device_name, device.get_pattern()).get_saves()

        previous_target_color = device_saves.get_target_pattern()

        target_pattern = self.get_configuration().get_properties().get_pattern()
        target_pattern_id = self.get_pattern_id(target_pattern)

        target_begin_since = device_saves.get_previous_pattern_duration()

        if previous_target_color != target_pattern_id or target_begin_since < 0:
            device_saves.set_target_pattern(*target_pattern_id) #type:ignore
            device_saves.set_new_previous_pattern_now(device.get_pattern())
            return
        
        target_duration = self._configuration.get_properties().get_transition_duration_time() / 1000
        base_device_pattern = device_saves.get_previous_pattern()

        if target_begin_since < target_duration:
            if isinstance(base_device_pattern, ComplexKeyboardColorPattern):
                colors = list(base_device_pattern.get_colors())

                for color_index in range(7):
                    color = colors[color_index]
                    target_color = target_pattern.get_colors()[color_index]

                    colors[color_index] = KeyboardColor.from_rgb(
                        int(color.get_red() * (1 - target_begin_since / target_duration) + target_color.get_red() * (target_begin_since / target_duration)),
                        int(color.get_green() * (1 - target_begin_since / target_duration) + target_color.get_green() * (target_begin_since / target_duration)),
                        int(color.get_blue() * (1 - target_begin_since / target_duration) + target_color.get_blue() * (target_begin_since / target_duration)),
                    )

                final_pattern = ComplexKeyboardColorPattern(*colors)
            
            elif isinstance(base_device_pattern, SimpleKeyboardColorPattern):
                current_color = base_device_pattern.get_color()

                colors = [current_color] * 7

                for color_index in range(7):
                    color = colors[color_index]
                    target_color = target_pattern.get_colors()[color_index]

                    colors[color_index] = KeyboardColor.from_rgb(
                        int(color.get_red() * (1 - target_begin_since / target_duration) + target_color.get_red() * (target_begin_since / target_duration)),
                        int(color.get_green() * (1 - target_begin_since / target_duration) + target_color.get_green() * (target_begin_since / target_duration)),
                        int(color.get_blue() * (1 - target_begin_since / target_duration) + target_color.get_blue() * (target_begin_since / target_duration)),
                    )

                final_pattern = ComplexKeyboardColorPattern(*colors)
            
            else:
                print("cannot find instance of", type(base_device_pattern))
                final_pattern = target_pattern
        else:
            final_pattern = target_pattern

        device.set_pattern(final_pattern)
    
    def stop(self) -> None:
        self._should_stop = True
    
