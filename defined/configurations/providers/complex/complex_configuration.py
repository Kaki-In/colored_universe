import configuration as _configuration

from .complex_properties import ComplexColorProviderProperties
from .complex_saves import ComplexColorProviderSaves

class ComplexConfiguration(_configuration.SettingsDirectory):
    def __init__(self, pathname: str, name: str) -> None:
        super().__init__(pathname)

        self._name = name

        self._properties = ComplexColorProviderProperties(self._create_sub_element_path("properties"))
        self._saves = ComplexColorProviderSaves(self._create_sub_element_path("saves"))

    def get_properties(self) -> ComplexColorProviderProperties:
        return self._properties
    
    def get_saves(self) -> ComplexColorProviderSaves:
        return self._saves

