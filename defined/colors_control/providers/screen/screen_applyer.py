import colors_control.objects as _colors_control_objects
import typing as _T

from .screen_provider import ScreenColorProvider, DISPLAY_AVAILABLE

class ScreenApplyer(_colors_control_objects.ProvidersScanner):
    def __init__(self) -> None:
        if DISPLAY_AVAILABLE:
            self._provider = ScreenColorProvider()

        else:
            self._provider = None

    def scan_for_providers(self) -> _T.Sequence[ScreenColorProvider]:
        if self._provider is None:
            return []

        return [self._provider]


