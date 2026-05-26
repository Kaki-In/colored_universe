import configuration as _configuration
import typing as _T
import os as _os

from .device_assignment_configuration import CasuisticDeviceAssignmentConfiguration

class CasuisticProviderCaseConfigurationDirectory(_configuration.SettingsDirectory):
    def __init__(self, pathname: str) -> None:
        super().__init__(pathname)

    def get_device_configuration(self, device_name: str, default_provider: str | None) -> CasuisticDeviceAssignmentConfiguration:
        return CasuisticDeviceAssignmentConfiguration(self._create_sub_element_path(device_name), default_provider)
    
    def get_known_devices(self) -> _T.Sequence[str]:
        return [filename[:-5] for filename in _os.listdir(self.get_pathname()) if _os.path.isfile(filename) and filename.endswith(".conf")]
    
