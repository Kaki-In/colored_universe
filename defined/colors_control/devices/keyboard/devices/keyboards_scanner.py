from colors_control.objects import DevicesScanner
from colors_control.objects.device import ColoredDevice
from colors_control.configuration.devices import DevicesScannersConfigurationDirectory

from defined.configurations.devices.keyboard.configuration import LocalColorKeyboardConfiguration

from .keyboard import LocalColorKeyboard

import subprocess as _subprocess
import typing as _T

class KeyboardsScanner(DevicesScanner):
    def __init__(self, devices: DevicesScannersConfigurationDirectory) -> None:
        super().__init__()

        self._device = None
        self._devices_directory = devices

        self.detect_device()

    def detect_device(self):
        try:
            found = "compatible keyboard found!" in _subprocess.getoutput("msiklm test").lower()

            if found: 
                found_devices = _subprocess.getoutput("msiklm list")

                devices_names = []

                for line in found_devices.split("\n"):
                    if line.startswith("Device: ") and "MSI" in line:
                        devices_names.append(line[len("Device: ") : ])

                if len(devices_names):
                    self._device = LocalColorKeyboard("Colored MSI Keyboard", 
                        LocalColorKeyboardConfiguration(
                            self._devices_directory.get_subdirectory_pathname("colored keyboard", devices_names[0]),
                            devices_names[0]
                        )
                    )

                    print("Compatible MSI keyboard has been found!")
        
        except Exception:
            pass

    def search_for_devices(self) -> _T.Sequence[ColoredDevice]:
        if self._device is None:
            return []
        
        else:
            return [self._device]



