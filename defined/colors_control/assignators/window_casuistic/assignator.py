import colors_control.objects as _colors_control

from defined.configurations.assignators import CasuisticConfigurationDirectory

from defined.thread_locks import XLIB_LOCK

class WindowCasuisticAssignator(_colors_control.DeviceProviderAssignator):
    def __init__(self, configuration: CasuisticConfigurationDirectory) -> None:
        super().__init__("window casuistic")

        self._configuration = configuration

    def get_current_window_name(self) -> str | None:
        import pywinctl as _pywinctl

        with XLIB_LOCK:
            active_window = _pywinctl.getActiveWindow()

            if active_window:
                return active_window.getAppName()
    
    def get_assigned_provider_for_device(self, device: _colors_control.ColoredDevice) -> str | None:
        try:
            window_name = self.get_current_window_name()
        except Exception as exc:
            return self._configuration.get_properties().get_default_provider()

        if window_name == None:
            return self._configuration.get_properties().get_default_provider()
        
        window_configuration = self._configuration.get_case_configuration(window_name)

        return window_configuration.get_device_configuration(device.get_device_name(), self._configuration.get_properties().get_default_provider()).get_assigned_provider()
    
    def accepts(self, device: _colors_control.ColoredDevice) -> bool:
        return True



