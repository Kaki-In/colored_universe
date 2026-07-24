from .device import ColoredDevice

from .devices_register import DevicesRegister
from .provider_register import ProvidersRegister

from .plugins_register import PluginsRegister

from ..configuration import *

import time as _time
import sys as _sys
import traceback as _traceback
import concurrent.futures as _concurrent_futures

class ColoredDevicesManager():
    def __init__(self, configuration: MainConfiguration) -> None:
        globals = {}

        self.__plugins = PluginsRegister(configuration.plugins_path, globals)

        self.__providers = ProvidersRegister(self.__plugins)
        self.__devices = DevicesRegister(self.__plugins)

        self.__configuration = configuration
        
        self.__executor = _concurrent_futures.ThreadPoolExecutor(max_workers=8)

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
    def provider_assignments(self) -> dict[str | None, list[ColoredDevice]]:
        providers_assignment: dict[str | None, list[ColoredDevice]] = { None: [] }

        assignators = self.__plugins.assignators

        for provider in self.__providers:
            providers_assignment[provider.name] = []

        for device in self.__devices:
            device_assignator = device.assignator_name

            found_provider = False
            
            for assignator in assignators:
                if assignator.name == device_assignator:
                    device_provider = assignator.get_assigned_provider_for_device(device)

                    if device_provider in providers_assignment:
                        providers_assignment[device_provider].append(device)
                        found_provider = True
                    
                    break
            
            if device_assignator is None or not found_provider:
                providers_assignment[None].append(device)

        return providers_assignment
    
    def refresh_providers_patterns(self) -> None:
        providers_assignment = self.provider_assignments

        futures = [
            self.__executor.submit(provider.apply_pattern, providers_assignment[provider.name])
            for provider in self.__providers
        ]

        for device in providers_assignment[None]:
            device.apply_no_pattern()
        
        _time.sleep(0.05)

        for future in futures:
            try:
                future.result(timeout=1)
            except Exception as exc:
                print("An error occured:", repr(exc), file=_sys.stderr, flush=True)
    
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
                
        except KeyboardInterrupt:
            status_control.mark_as_stopped()
            raise

        except BaseException:
            status_control.mark_as_stopped(_traceback.format_exc())
            raise
        
        else:
            status_control.mark_as_stopped()



    
