from .color_provider import ColorProvider

from .plugins_register import PluginsRegister

import typing as _T

class ProvidersRegister():
    def __init__(self, plugins: PluginsRegister) -> None:
        self.__plugins = plugins
        self.__found_providers: dict[str, ColorProvider] = {}

    def scan_for_providers(self) -> _T.Sequence[ColorProvider]:
        found_providers = []

        for scanner in self.__plugins.providers_scanners:
            found_providers.extend(scanner.scan_for_providers())

        return found_providers
    
    def get_found_providers(self) -> _T.Sequence[ColorProvider]:
        return list(self.__found_providers.values())
    
    def reload_providers(self) -> tuple[_T.Sequence[ColorProvider], _T.Sequence[ColorProvider]]:
        scanned_providers = self.scan_for_providers()

        current_providers_names = list(self.__found_providers.keys())
        scanned_providers_names = [provider.name for provider in scanned_providers]

        new_providers: _T.Sequence[ColorProvider] = []
        deleted_providers: _T.Sequence[ColorProvider] = []

        for possibly_new_provider in scanned_providers:
            if not possibly_new_provider.name in current_providers_names:
                new_providers.append(possibly_new_provider)
        
        for possibly_old_provider in self.__found_providers.values():
            if not possibly_old_provider.name in scanned_providers_names:
                deleted_providers.append(possibly_old_provider)
        
        self.__found_providers = {}

        for provider in scanned_providers:
            self.__found_providers[provider.name] = provider
        
        return new_providers, deleted_providers
    
    @property
    def provider_names(self) -> _T.Sequence[str]:
        return list(self.__found_providers)
    
    def get_provider_by_name(self, name: str) -> ColorProvider:
        if not name in self.__found_providers:
           raise ReferenceError("no such provider")
        
        return self.__found_providers[name]
            
    def provider_is_known(self, name: str) -> bool:
        return name in self.__found_providers
    
    def get_provider_by_type[ProviderType: ColorProvider](self, class_type: _T.Type[ProviderType], is_strict=False) -> _T.Sequence[ProviderType]:
        found_providers: list[ProviderType] = []

        for provider in self.__found_providers:
            if is_strict:
                condition = type(provider) == class_type
            else:
                condition = isinstance(provider, class_type)

            if condition:
                found_providers.append(provider) # type:ignore because the condition ensures that provider is compatible
        
        return found_providers
    
    def __iter__(self) -> _T.Iterator[ColorProvider]:
        return iter(self.__found_providers.values())

