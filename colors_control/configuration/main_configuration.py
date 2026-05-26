import configuration as _configuration
import os as _os

from .providers import ProvidersScannersConfigurationDirectory
from .devices import DevicesScannersConfigurationDirectory
from .assignators import AssignatorsConfigurationDirectory

from .status_control import StatusControlConfiguration

DEFAULT_CONF_DIR = _os.environ["HOME"] + _os.path.sep + ".colored_universe"

class MainConfiguration(_configuration.SettingsDirectory):
    def __init__(self) -> None:
        super().__init__(DEFAULT_CONF_DIR)

        self._providers_configuration = ProvidersScannersConfigurationDirectory(self._create_sub_element_path("providers"))
        self._devices_configuration = DevicesScannersConfigurationDirectory(self._create_sub_element_path("devices"))
        self._assignators_configuration = AssignatorsConfigurationDirectory(self._create_sub_element_path("assignators"))

        self._status_control = StatusControlConfiguration(self._create_sub_element_path("status_control"))
    
    def get_providers_configuration(self) -> ProvidersScannersConfigurationDirectory:
        return self._providers_configuration
    
    def get_devices_configuration(self) -> DevicesScannersConfigurationDirectory:
        return self._devices_configuration
    
    def get_assignators_configuration(self) -> AssignatorsConfigurationDirectory:
        return self._assignators_configuration
    
    def get_plugins_path(self) -> str:
        return self._create_sub_element_path("plugins")
    
    def get_status_control(self) -> StatusControlConfiguration:
        return self._status_control
    
    
