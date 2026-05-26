import configuration as _configuration
import os as _os
import typing as _T

class DevicesScannersConfigurationDirectory(_configuration.SettingsDirectory):
    def __init__(self, pathname: str) -> None:
        super().__init__(pathname)

    def get_subdirectory_pathname(self, provider_name:str, name: str) -> str:
        return self._create_sub_element_path(provider_name + ":" + name)
    


