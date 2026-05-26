import colors_control.objects as _colors_control_objects
import typing as _T

from .windowed import WindowedColorProvider, DISPLAY_AVAILABLE

class WindowApplyer(_colors_control_objects.ProvidersScanner):
    def __init__(self) -> None:
        if DISPLAY_AVAILABLE:
            self._provider = WindowedColorProvider()

        else:
            self._provider = None

    def scan_for_providers(self) -> _T.Sequence[WindowedColorProvider]:
        if self._provider is None:
            return []

        return [self._provider]


