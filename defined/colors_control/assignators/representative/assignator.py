import colors_control.objects as _colors_control

from defined.configurations.assignators import RepresentativeAssignatorDirectory

class RepresentativeAssignator(_colors_control.DeviceProviderAssignator):
    def __init__(self, configuration: RepresentativeAssignatorDirectory) -> None:
        super().__init__("representative")

        self._configuration = configuration

    def get_assigned_provider_for_device(self, device: _colors_control.ColoredDevice) -> str | None:
        return self._configuration.get_device_assignment(device.get_device_name()).get_assigned_provider()


