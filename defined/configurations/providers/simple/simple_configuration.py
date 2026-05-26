import configuration as _configuration

from .simple_properties import SimpleColorProviderProperties
from .simple_saves import SimpleColorProviderSaves

class SimpleConfiguration(_configuration.SettingsDirectory):
    def __init__(self, pathname: str, name: str) -> None:
        super().__init__(pathname)

        self._name = name

        self._properties = SimpleColorProviderProperties(self._create_sub_element_path("properties"))
        self._saves = SimpleColorProviderSaves(self._create_sub_element_path("saves"))

    def get_properties(self) -> SimpleColorProviderProperties:
        return self._properties
    
    def get_saves(self) -> SimpleColorProviderSaves:
        return self._saves

