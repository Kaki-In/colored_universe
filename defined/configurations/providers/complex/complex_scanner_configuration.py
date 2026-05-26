import configuration as _configuration
import os as _os
import typing as _T

from .complex_configuration import ComplexConfiguration

class ComplexProvidersScannerConfiguration(_configuration.SettingsDirectory):
    def __init__(self, pathname: str) -> None:
        super().__init__(pathname)

    def get_defined_colors(self) -> _T.Sequence[str]:
        files = _os.listdir(self.get_pathname())

        dirs: list[str] = []
        
        for file in files:
            if _os.path.isdir(self._create_sub_element_path(file)):
                dirs.append(file)
        
        return dirs
    
    def create_color(self) -> ComplexConfiguration:
        a = 0

        get_color_name = lambda: "Color " + ("0" * (4 - len(str(a)))) + str(a)
        dirs = _os.listdir(self._pathname)

        while get_color_name() in dirs:
            a += 1
        
        color_name = get_color_name()
        
        return ComplexConfiguration(self._create_sub_element_path(color_name), color_name)
    
    def get_color_configuration(self, color_name: str) -> ComplexConfiguration:
        return ComplexConfiguration(self._create_sub_element_path(color_name), color_name)

