import configuration as _configuration
import os as _os
import shutil as _shutil

from .devices import SimpleColorProviderSavedDeviceDirectory
from defined.colors_control.devices.keyboard.patterns import KeyboardPattern

class SimpleColorProviderSaves(_configuration.SettingsDirectory):
    def __init__(self, path: str) -> None:
        super().__init__(path)

    def get_device_save(self, device_name: str, default_pattern: KeyboardPattern) -> SimpleColorProviderSavedDeviceDirectory:
        return SimpleColorProviderSavedDeviceDirectory(self._create_sub_element_path(device_name), default_pattern)
    
    def get_known_devices(self) -> list[str]:
        return [path for path in _os.listdir(self.get_pathname()) if _os.path.isdir(self._create_sub_element_path(path))]
    
    def forget_device(self, device_name: str) -> None:
        if not device_name in _os.listdir(self.get_pathname()):
            return

        try:
            _shutil.rmtree(self._create_sub_element_path(device_name))
        except Exception as exc:
            pass

