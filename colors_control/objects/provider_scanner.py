from .color_provider import ColorProvider

import typing as _T

class ProvidersScanner():
    def scan_for_providers(self) -> _T.Sequence[ColorProvider]:
        raise NotImplementedError("not implemented for " + repr(self))


