from ..enums.modeidentifier import KeyboardModeIdentifier

class KeyboardMode():
    def __init__(self, mode: KeyboardModeIdentifier):
        self._mode = mode
    
    def get_mode(self) -> KeyboardModeIdentifier:
        return self._mode

    def __str__(self) -> str:
        return self._mode.value

