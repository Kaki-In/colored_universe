from .color_provider import ColorProvider
from .device import ColoredDevice

from .devices_register import DevicesRegister
from .provider_register import ProvidersRegister
from .provider_assignator import DeviceProviderAssignator

from .plugins_register import PluginsRegister

from ..configuration import *

import time as _time
import threading as _threading
import sys as _sys
import typing as _T

class ColoredDevicesManager():
    def __init__(self, configuration: MainConfiguration) -> None:
        globals = {}

        self._plugins = PluginsRegister(configuration.get_plugins_path(), globals)

        self._providers = ProvidersRegister(self._plugins)
        self._devices = DevicesRegister(self._plugins)

        self._configuration = configuration

        globals["PROVIDERS"] = self._providers
        globals["DEVICES"] = self._devices
        globals["MAIN_CONFIGURATION"] = self._configuration

    def get_providers(self) -> ProvidersRegister:
        return self._providers
    
    def get_plugins(self) -> PluginsRegister:
        return self._plugins
    
    def get_devices(self) -> DevicesRegister:
        return self._devices
    
    def refresh_devices(self) -> None:
        new_devices, deleted_devices = self._devices.reload_devices()

        for old_device in deleted_devices:
            old_device.on_expulsed()

        for new_device in new_devices:
            new_device.on_integrated()
        
    def refresh_providers(self) -> None:
        new_providers, deleted_providers = self._providers.reload_providers()

        for old_provider in deleted_providers:
            old_provider.on_terminate()
        
        for new_provider in new_providers:
            new_provider.on_start()
        
    def get_configuration(self) -> MainConfiguration:
        return self._configuration
    
    def get_provider_assignments(self) -> dict[str, list[ColoredDevice]]:
        providers_assignment: dict[str, list[ColoredDevice]] = {}

        assignators = self._plugins.get_assignators()

        for provider in self._providers:
            providers_assignment[provider.get_name()] = []

        for device in self._devices:
            device_assignator = device.get_assignator_name()

            for assignator in assignators:
                if assignator.get_name() == device_assignator:
                    device_provider = assignator.get_assigned_provider_for_device(device)

                    if device_provider in providers_assignment:
                        providers_assignment[device_provider].append(device)
                    
                    break

        return providers_assignment
    
    def refresh_providers_patterns(self) -> None:
        providers_assignment = self.get_provider_assignments()

        threads: list[tuple[_threading.Thread, ColorProvider]] = []

        for provider in self._providers:
            devices = providers_assignment[provider.get_name()]

            thread = _threading.Thread(target=provider.apply_pattern, args=(devices,))
            threads.append((thread, provider))
        
        for thread, _ in threads:
            thread.start()

        _time.sleep(0.01)
            
        for thread, provider in threads:
            try:
                if thread.is_alive():
                    thread.join(timeout=1)

            except Exception as exc:
                print(
                    "An error occured while joining to thread", thread, ":", repr(exc),
                    file=_sys.stderr,
                    flush=True
                )
    
    def refresh_plugins(self) -> None:
        self._plugins.reload()

    def main(self) -> None:
        status_control = self._configuration.get_status_control()

        status_control.mark_as_running()

        try:
            while not status_control.requires_for_stop():
                self.refresh_plugins()

                self.refresh_devices()
                self.refresh_providers()

                self.refresh_providers_patterns()
        except Exception as exc:
            status_control.mark_as_stopped(str(exc))
            raise

        else:
            status_control.mark_as_stopped()



    
