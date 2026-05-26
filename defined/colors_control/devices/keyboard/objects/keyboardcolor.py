from colors_control.objects import Color

class KeyboardColor(Color):
    def __init__(self, name: str, red: int, green: int, blue: int) -> None:
        super().__init__(name, red, green, blue)
    
    @staticmethod
    def from_rgb(r: int, g: int, b: int) -> 'KeyboardColor':
        true_color = r * (255 ** 2) + g * (255) + b
        true_color_hex = hex(true_color)[2:]

        if r < 0:
            raise

        return KeyboardColor("0x" + "0"*(6 - len(true_color_hex)) + true_color_hex, r, g, b)
    
    def __str__(self) -> str:
        return "'[{};{};{}]'".format(self._red, self._green, self._blue)

KEYBOARD_COLOR_RED = KeyboardColor("red", 255, 0, 0)
KEYBOARD_COLOR_ORANGE = KeyboardColor("orange", 255, 170, 0)
KEYBOARD_COLOR_YELLOW = KeyboardColor("yellow", 255, 255, 0)
KEYBOARD_COLOR_GREEN = KeyboardColor("green", 0, 255, 0)
KEYBOARD_COLOR_CYAN = KeyboardColor("sky", 0, 255, 255)
KEYBOARD_COLOR_BLUE = KeyboardColor("blue", 0, 0, 255)
KEYBOARD_COLOR_MAGENTA = KeyboardColor("purple", 255, 0, 255)
KEYBOARD_COLOR_WHITE = KeyboardColor("white", 255, 255, 255)
KEYBOARD_COLOR_BLACK = KeyboardColor("off", 0, 0, 0)
KEYBOARD_COLOR_NONE = KeyboardColor("none", 0, 0, 0)

