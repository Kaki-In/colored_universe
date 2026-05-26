from .color_provider import ColorProvider

import typing as _T
import abc as _abc

class ProvidersScanner(_abc.ABC):
    @_abc.abstractmethod
    def scan_for_providers(self) -> _T.Sequence[ColorProvider]:
        ...


