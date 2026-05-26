from ..enums.brightnessidentifier import KeyboardBrightnessIdentifier

class KeyboardBrightness():
    def __init__(self, brightness: KeyboardBrightnessIdentifier) -> None:
        self._brightness = brightness
    
    def get_brightness(self) -> KeyboardBrightnessIdentifier:
        return self._brightness

    def __str__(self) -> str:
        return self._brightness

