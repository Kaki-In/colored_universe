import configuration as _configuration
import typing as _T

from .device_assignment_object import RepresentativeDeviceAssignmentObject

class RepresentativeDeviceAssignmentConfiguration(_configuration.SettingsFile[RepresentativeDeviceAssignmentObject]):
    def __init__(self, path: str, default_provider: _T.Optional[str] = None) -> None:
        super().__init__(path, {
            "assigned_provider": default_provider
        })

    def get_assigned_provider(self) -> str | None:
        return self.get_content()["assigned_provider"]


