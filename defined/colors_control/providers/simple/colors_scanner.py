import colors_control.objects as _colors_control

import defined.configurations.providers.simple as _simple_configuration
import typing as _T

from .simple_provider import SimpleColorProvider

class SimpleColorProvidersScanner(_colors_control.ProvidersScanner):
    def __init__(self, configuration: _simple_configuration.SimpleProvidersScannerConfiguration) -> None:
        super().__init__()

        self._configuration = configuration

    def get_configuration(self) -> _simple_configuration.SimpleProvidersScannerConfiguration:
        return self._configuration
    
    def get_created_colors(self) -> _T.Sequence[SimpleColorProvider]:
        colors = self._configuration.get_defined_colors()

        returned_providers: list[SimpleColorProvider] = []

        for color_name in colors:
            returned_providers.append(
                SimpleColorProvider(color_name, self._configuration.get_color_configuration(color_name))
            )

        return returned_providers

    def scan_for_providers(self) -> _T.Sequence[SimpleColorProvider]:
        return self.get_created_colors()



