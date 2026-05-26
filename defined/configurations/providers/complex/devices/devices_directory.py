import configuration as _configuration

from .device_save import ComplexColorProviderDeviceSaves
from defined.colors_control.devices.keyboard.patterns import KeyboardPattern

class ComplexColorProviderSavedDeviceDirectory(_configuration.SettingsDirectory):
    def __init__(self, pathname: str, default_pattern: KeyboardPattern) -> None:
        super().__init__(pathname)

        self._saves = ComplexColorProviderDeviceSaves(self._create_sub_element_path("saves"), default_pattern)

    def get_saves(self) -> ComplexColorProviderDeviceSaves:
        return self._saves

