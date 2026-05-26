import configuration as _configuration

class ProvidersScannersConfigurationDirectory(_configuration.SettingsDirectory):
    def __init__(self, pathname: str):
        super().__init__(pathname)

    def get_subdirectory_pathname(self, name: str) -> str:
        return self._create_sub_element_path(name)


