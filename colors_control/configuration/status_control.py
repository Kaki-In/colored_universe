import configuration as _configuration
import typing as _T

from ..configuration_objects import StatusControlObject

class StatusControlConfiguration(_configuration.SettingsFile[StatusControlObject]):
    def __init__(self, path: str) -> None:
        super().__init__(path, {
            'is_running': False,
            'required_for_stop': False,
            'stopped_error': None
        })
    
    def mark_as_running(self) -> None:
        self.overwrite({
            'is_running': True,
            'required_for_stop': False,
            'stopped_error': None
        })

    def mark_as_stopped(self, error: _T.Optional[str] = None) -> None:
        self.overwrite({
            'is_running': False,
            'required_for_stop': False,
            'stopped_error': error
        })

    def requires_for_stop(self) -> bool:
        return self.get_content()['required_for_stop']


