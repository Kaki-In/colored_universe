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

        self._plugins: dict[str, Plugin] = {}
        self._builder = PluginBuilder(pathname, globals)

    def get_devices_scanners(self) -> _T.Sequence[DevicesScanner]:
        scanners: list[DevicesScanner] = []

        for plugin in self._plugins.values():
            scanners += plugin.get_devices_scanners()

        return scanners

    def get_providers_scanners(self) -> _T.Sequence[ProvidersScanner]:
        scanners: list[ProvidersScanner] = []

        for plugin in self._plugins.values():
            scanners += plugin.get_providers_scanners()

        return scanners

    def get_assignators(self) -> _T.Sequence[DeviceProviderAssignator]:
        assignators: list[DeviceProviderAssignator] = []

        for plugin in self._plugins.values():
            assignators += plugin.get_assignators()

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
            if not new_plugin_name in self._plugins:
                plugin = self._builder.load_plugin(new_plugin_name)
                new_plugins.append(plugin)

                self._plugins[new_plugin_name] = plugin

                print("added plugin", plugin.get_name())

                print("Device scanners:", plugin.get_devices_scanners())
                print("Provider scanners:", plugin.get_providers_scanners())
                print("Assignators:", [assignator.get_name() for assignator in plugin.get_assignators()])

        for old_plugin_name in self._plugins.copy():
            if not old_plugin_name in defined_plugins:
                deleted_plugins.append(self._plugins[old_plugin_name])

                print("deleted plugin", old_plugin_name)

                del self._plugins[old_plugin_name]
        
        for plugin in self._plugins.values():
            if plugin.get_hash() != self._builder.get_current_hash(plugin.get_pathname()):
                modified_plugins.append(plugin)

                plugins = self._builder.reload_plugin(plugin.get_pathname())

                for plugin in plugins:
                    self._plugins[plugin.get_pathname()] = plugin

                print("modified plugin", plugin.get_name())

        return new_plugins, modified_plugins, deleted_plugins
    
    def get_plugin_names(self) -> _T.Sequence[str]:
        return list(self._plugins.keys())
    
    def get_plugins(self) -> _T.Sequence[Plugin]:
        return list(self._plugins.values())
    
    def get_plugin_by_name(self, name: str) -> Plugin:
        return self._plugins[name]
 



