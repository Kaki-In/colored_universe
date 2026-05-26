from .provider_scanner import ProvidersScanner
from .color_provider import ColorProvider

from .plugins_register import PluginsRegister

import typing as _T

class ProvidersRegister():
    def __init__(self, plugins: PluginsRegister) -> None:
        self._plugins = plugins
        self._found_providers: dict[str, ColorProvider] = {}

    def scan_for_providers(self) -> _T.Sequence[ColorProvider]:
        found_providers = []

        for scanner in self._plugins.get_providers_scanners():
            found_providers.extend(scanner.scan_for_providers())

        return found_providers
    
    def get_found_providers(self) -> _T.Sequence[ColorProvider]:
        return list(self._found_providers.values())
    
    def reload_providers(self) -> tuple[_T.Sequence[ColorProvider], _T.Sequence[ColorProvider]]:
        scanned_providers = self.scan_for_providers()

        current_providers_names = list(self._found_providers.keys())
        scanned_providers_names = [provider.get_name() for provider in scanned_providers]

        new_providers: _T.Sequence[ColorProvider] = []
        deleted_providers: _T.Sequence[ColorProvider] = []

        for possibly_new_provider in scanned_providers:
            if not possibly_new_provider.get_name() in current_providers_names:
                new_providers.append(possibly_new_provider)
        
        for possibly_old_provider in self._found_providers.values():
            if not possibly_old_provider.get_name() in scanned_providers_names:
                deleted_providers.append(possibly_old_provider)
        
        self._found_providers = {}

        for provider in scanned_providers:
            self._found_providers[provider.get_name()] = provider
        
        return new_providers, deleted_providers
    
    def get_provider_names(self) -> _T.Sequence[str]:
        return list(self._found_providers)
    
    def get_provider_by_name(self, name: str) -> ColorProvider:
        if not name in self._found_providers:
           raise ReferenceError("no such provider")
        
        return self._found_providers[name]
            
    def provider_is_known(self, name: str) -> bool:
        return name in self._found_providers
    
    def get_provider_by_type[ProviderType: ColorProvider](self, class_type: _T.Type[ProviderType], is_strict=False) -> _T.Sequence[ProviderType]:
        found_providers: list[ProviderType] = []

        for provider in self._found_providers:
            if is_strict:
                condition = type(provider) == class_type
            else:
                condition = isinstance(provider, class_type)

            if condition:
                found_providers.append(provider) # type:ignore because the condition ensures that provider is compatible
        
        return found_providers
    
    def __iter__(self) -> _T.Iterator[ColorProvider]:
        return iter(self._found_providers.values())

