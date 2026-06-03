import configuration as _configuration
import os as _os

from .providers import ProvidersScannersConfigurationDirectory
from .devices import DevicesScannersConfigurationDirectory
from .assignators import AssignatorsConfigurationDirectory

from .status_control import StatusControlConfiguration

class MainConfiguration(_configuration.SettingsDirectory):
    def __init__(self, path: str) -> None:
        super().__init__(path)

        self.__providers_configuration = ProvidersScannersConfigurationDirectory(self._create_sub_element_path("providers"))
        self.__devices_configuration = DevicesScannersConfigurationDirectory(self._create_sub_element_path("devices"))
        self.__assignators_configuration = AssignatorsConfigurationDirectory(self._create_sub_element_path("assignators"))

        self.__status_control = StatusControlConfiguration(self._create_sub_element_path("status_control"))
    
    @property
    def providers_configuration(self) -> ProvidersScannersConfigurationDirectory:
        return self.__providers_configuration
    
    @property
    def devices_configuration(self) -> DevicesScannersConfigurationDirectory:
        return self.__devices_configuration
    
    @property
    def assignators_configuration(self) -> AssignatorsConfigurationDirectory:
        return self.__assignators_configuration
    
    @property
    def plugins_path(self) -> str:
        return self._create_sub_element_path("plugins")
    
    @property
    def status_control(self) -> StatusControlConfiguration:
        return self.__status_control
    
    
