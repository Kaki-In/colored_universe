import configuration as _configuration

from .keyboard_conf import KeyboardConfigurationFile

class LocalColorKeyboardConfiguration(_configuration.SettingsDirectory):
    def __init__(self, pathname: str, name:str) -> None:
        super().__init__(pathname)

        self._name = name
        
        self._configuration = KeyboardConfigurationFile(self._create_sub_element_path("properties"))

    def get_configuration(self) -> KeyboardConfigurationFile:
        return self._configuration


