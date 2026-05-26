import configuration as _configuration

from .casuistic_properties_object import CasuisticPropertiesObject

class CasuisticProviderProperties(_configuration.SettingsFile[CasuisticPropertiesObject]):
    def __init__(self, path: str) -> None:
        super().__init__(path, {
            'default_provider': None
        })

    def get_default_provider(self) -> str | None:
        return self.get_content()['default_provider']
    
    def set_default_provider(self, provider: str | None) :
        content = self.get_content()

        content['default_provider'] = provider

        self.overwrite(content)

