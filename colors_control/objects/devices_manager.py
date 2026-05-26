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

class ColoredDevicesManager():
    def __init__(self, configuration: MainConfiguration) -> None:
        globals = {}

        self.__plugins = PluginsRegister(configuration.plugins_path, globals)

        self.__providers = ProvidersRegister(self.__plugins)
        self.__devices = DevicesRegister(self.__plugins)

        self.__configuration = configuration

        globals["PROVIDERS"] = self.__providers
        globals["DEVICES"] = self.__devices
        globals["MAIN_CONFIGURATION"] = self.__configuration

    @property
    def providers(self) -> ProvidersRegister:
        return self.__providers
    
    @property
    def plugins(self) -> PluginsRegister:
        return self.__plugins
    
    @property
    def devices(self) -> DevicesRegister:
        return self.__devices
    
    def refresh_devices(self) -> None:
        new_devices, deleted_devices = self.__devices.reload_devices()

        for old_device in deleted_devices:
            old_device.on_expulsed()

        for new_device in new_devices:
            new_device.on_integrated()
        
    def refresh_providers(self) -> None:
        new_providers, deleted_providers = self.__providers.reload_providers()

        for old_provider in deleted_providers:
            old_provider.on_terminate()
        
        for new_provider in new_providers:
            new_provider.on_start()
        
    @property
    def configuration(self) -> MainConfiguration:
        return self.__configuration
    
    @property
    def provider_assignments(self) -> dict[str, list[ColoredDevice]]:
        providers_assignment: dict[str, list[ColoredDevice]] = {}

        assignators = self.__plugins.assignators

        for provider in self.__providers:
            providers_assignment[provider.name] = []

        for device in self.__devices:
            device_assignator = device.assignator_name

            for assignator in assignators:
                if assignator.name == device_assignator:
                    device_provider = assignator.get_assigned_provider_for_device(device)

                    if device_provider in providers_assignment:
                        providers_assignment[device_provider].append(device)
                    
                    break

        return providers_assignment
    
    def refresh_providers_patterns(self) -> None:
        providers_assignment = self.provider_assignments

        threads: list[tuple[_threading.Thread, ColorProvider]] = []

        for provider in self.__providers:
            devices = providers_assignment[provider.name]

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
        self.__plugins.reload()

    def main(self) -> None:
        status_control = self.__configuration.status_control

        status_control.mark_as_running()

        try:
            while not status_control.requires_for_stop:
                self.refresh_plugins()

                self.refresh_devices()
                self.refresh_providers()

                self.refresh_providers_patterns()
        except Exception as exc:
            status_control.mark_as_stopped(str(exc))
            raise

        else:
            status_control.mark_as_stopped()



    
