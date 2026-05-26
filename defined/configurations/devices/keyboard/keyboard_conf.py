import configuration as _configuration

from .keyboard_conf_object import KeyboardConfigurationObject

class KeyboardConfigurationFile(_configuration.SettingsFile[KeyboardConfigurationObject]):
    def __init__(self, path: str) -> None:
        super().__init__(path, {
            'assignator': None
        })
    
    def get_assigned_provider(self) -> str | None:
        return self.get_content()['assignator']
    
    def set_assigned_provider(self, provider: str | None) -> None:
        content = self.get_content()
        content['assignator'] = provider

        self.overwrite(content)

