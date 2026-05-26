from .device import ColoredDevice

from .plugins_register import PluginsRegister

import time as _time
import sys as _sys
import typing as _T

class DevicesRegister():
    def __init__(self, plugins: PluginsRegister) -> None:
        self.__plugins = plugins
        self.__found_devices: list[ColoredDevice] = []

    def scan_devices(self) -> _T.Sequence[ColoredDevice]:
        found_devices: _T.Sequence[ColoredDevice] = []

        for scanner in self.__plugins.devices_scanners:
            start_time = _time.monotonic()

            found_devices.extend(scanner.search_for_devices())

            stop_time = _time.monotonic()

            if stop_time - start_time > 0.1:
                print("Warning : devices scan for", scanner, "took", stop_time - start_time, "seconds to scan", file=_sys.stderr, flush=True)
        
        return found_devices
    
    @property
    def found_devices(self) -> _T.Sequence[ColoredDevice]:
        return self.__found_devices
    
    def reload_devices(self) -> tuple[_T.Sequence[ColoredDevice], _T.Sequence[ColoredDevice]]:
        scanned_devices = self.scan_devices()

        current_devices_names = [device.device_name for device in self.__found_devices]
        scanned_devices_names = [device.device_name for device in scanned_devices]

        new_devices: _T.Sequence[ColoredDevice] = []
        deleted_devices: _T.Sequence[ColoredDevice] = []

        for possibly_new_device in scanned_devices:
            if not possibly_new_device.device_name in current_devices_names:
                new_devices.append(possibly_new_device)
        
        for possibly_old_device in self.__found_devices:
            if not possibly_old_device.device_name in scanned_devices_names:
                deleted_devices.append(possibly_old_device)

        self.__found_devices = list(scanned_devices)
        
        return new_devices, deleted_devices
    
    def get_device_by_name(self, name: str) -> ColoredDevice:
        for device in self.__found_devices:
            if device.device_name == name:
                return device
            
        raise ReferenceError("no such device")
    
    def get_device_names(self) -> _T.Sequence[str]:
        return [device.device_name for device in self.__found_devices]
    
    def device_is_known(self, name: str) -> bool:
        for device in self.__found_devices:
            if device.device_name == name:
                return True
            
        return False
    
    def get_devices_by_class[DeviceType: ColoredDevice](self, class_type: _T.Type[DeviceType], is_strict=False) -> _T.Sequence[DeviceType]:
        found_devices: _T.Sequence[DeviceType] = []

        for device in self.__found_devices:
            if is_strict:
                condition = type(device) == class_type
            else:
                condition = isinstance(device, class_type)

            if condition:
                found_devices.append(device) # type:ignore because the condition ensures that device is compatible
        
        return found_devices
    
    def __iter__(self) -> _T.Iterator[ColoredDevice]:
        return iter(self.__found_devices)

