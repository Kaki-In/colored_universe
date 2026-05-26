import configuration as _configuration
import typing as _T
import os as _os
import shutil as _shutil

from .casuistic_case.casuistic_case_directory import CasuisticProviderCaseConfigurationDirectory
from .casuistic_properties import CasuisticProviderProperties

class CasuisticConfigurationDirectory(_configuration.SettingsDirectory):
    def __init__(self, pathname: str) -> None:
        super().__init__(pathname)

        self._properties = CasuisticProviderProperties(self._create_sub_element_path("properties"))

    def get_properties(self) -> CasuisticProviderProperties:
        return self._properties

    def name_to_dirname(self, name: str) -> str:
        return name.replace("_", "_u").replace("/", "_s")
    
    def dirname_to_name(self, dirname: str) -> str:
        return dirname.replace("_s", "/").replace("_u", "_")

    def get_known_cases(self) -> _T.Sequence[str]:
        return [self.dirname_to_name(dirname) for dirname in _os.listdir(self.get_pathname()) if _os.path.isdir(dirname)]
    
    def get_case_configuration(self, case: str) -> CasuisticProviderCaseConfigurationDirectory:
        return CasuisticProviderCaseConfigurationDirectory(self._create_sub_element_path(self.name_to_dirname(case)))
    
    def forget_case(self, case: str) -> None:
        _shutil.rmtree(self._create_sub_element_path(self.name_to_dirname(case)))


