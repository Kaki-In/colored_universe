import colors_control.objects as _colors_control

import defined.configurations.providers.complex as _complex_configuration
import typing as _T

from .complex_provider import ComplexColorProvider

class ComplexColorProvidersScanner(_colors_control.ProvidersScanner):
    def __init__(self, configuration: _complex_configuration.ComplexProvidersScannerConfiguration) -> None:
        super().__init__()

        self._configuration = configuration

    def get_configuration(self) -> _complex_configuration.ComplexProvidersScannerConfiguration:
        return self._configuration
    
    def get_created_colors(self) -> _T.Sequence[ComplexColorProvider]:
        colors = self._configuration.get_defined_colors()

        returned_providers: list[ComplexColorProvider] = []

        for color_name in colors:
            returned_providers.append(
                ComplexColorProvider(color_name, self._configuration.get_color_configuration(color_name))
            )

        return returned_providers

    def scan_for_providers(self) -> _T.Sequence[ComplexColorProvider]:
        return self.get_created_colors()



