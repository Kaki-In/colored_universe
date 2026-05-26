from .plugin import Plugin
from .plugin_builder import PluginBuilder

from .device_scanner import DevicesScanner
from .provider_scanner import ProvidersScanner
from .provider_assignator import DeviceProviderAssignator

import configuration as _configuration
import os as _os
import typing as _T

class PluginsRegister(_configuration.SettingsDirectory):
    def __init__(self, pathname: str, globals: dict) -> None:
        super().__init__(pathname)

        self.__plugins: dict[str, Plugin] = {}
        self.__builder = PluginBuilder(pathname, globals)

    @property
    def devices_scanners(self) -> _T.Sequence[DevicesScanner]:
        scanners: list[DevicesScanner] = []

        for plugin in self.__plugins.values():
            scanners += plugin.devices_scanners

        return scanners

    @property
    def providers_scanners(self) -> _T.Sequence[ProvidersScanner]:
        scanners: list[ProvidersScanner] = []

        for plugin in self.__plugins.values():
            scanners += plugin.providers_scanners

        return scanners

    @property
    def assignators(self) -> _T.Sequence[DeviceProviderAssignator]:
        assignators: list[DeviceProviderAssignator] = []

        for plugin in self.__plugins.values():
            assignators += plugin.assignators

        return assignators

    def reload(self) -> tuple[_T.Sequence[Plugin], _T.Sequence[Plugin], _T.Sequence[Plugin]]:
        defined_plugins = []

        new_plugins: list[Plugin] = []
        modified_plugins: list[Plugin] = []
        deleted_plugins: list[Plugin] = []

        for plugin_name in _os.listdir(self.get_pathname()):
            if _os.path.isfile(self._create_sub_element_path(plugin_name)) and plugin_name.endswith(".crp"):
                defined_plugins.append(plugin_name)

        for new_plugin_name in defined_plugins.copy():
            if not new_plugin_name in self.__plugins:
                plugin = self.__builder.load_plugin(new_plugin_name)
                new_plugins.append(plugin)

                self.__plugins[new_plugin_name] = plugin

                print("added plugin", plugin.name)

                print("Device scanners:", plugin.devices_scanners)
                print("Provider scanners:", plugin.providers_scanners)
                print("Assignators:", [assignator.name for assignator in plugin.assignators])

        for old_plugin_name in self.__plugins.copy():
            if not old_plugin_name in defined_plugins:
                deleted_plugins.append(self.__plugins[old_plugin_name])

                print("deleted plugin", old_plugin_name)

                del self.__plugins[old_plugin_name]
        
        for plugin in self.__plugins.values():
            if plugin.hash != self.__builder.get_current_hash(plugin.pathname):
                modified_plugins.append(plugin)

                plugins = self.__builder.reload_plugin(plugin.pathname)

                for plugin in plugins:
                    self.__plugins[plugin.pathname] = plugin

                print("modified plugin", plugin.name)

        return new_plugins, modified_plugins, deleted_plugins
    
    @property
    def plugin_names(self) -> _T.Sequence[str]:
        return list(self.__plugins.keys())
    
    @property
    def plugins(self) -> _T.Sequence[Plugin]:
        return list(self.__plugins.values())
    
    def get_plugin_by_name(self, name: str) -> Plugin:
        return self.__plugins[name]
 



