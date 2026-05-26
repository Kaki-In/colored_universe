from colors_control.objects import ColorProvider, ColoredDevice, Color

from defined.colors_control.devices.keyboard.devices import *
from defined.colors_control.devices.keyboard.patterns import *
from defined.colors_control.devices.keyboard.objects import *

import typing as _T

import PIL.Image as _pil_image

try:
    import pyautogui as _pyautogui
    DISPLAY_AVAILABLE = True

except:
    DISPLAY_AVAILABLE = False

class ScreenColorProvider(ColorProvider):
    def __init__(self) -> None:
        super().__init__("Screen Based Color", '')

    def can_handle(self, device: ColoredDevice) -> bool:
        return isinstance(device, LocalColorKeyboard)
    
    def capture_pattern(self) -> ComplexKeyboardColorPattern:
        import pyautogui as _pyautogui
        
        image = _pyautogui.screenshot()

        image_width, image_height = image.size

        image_left = image.crop((0, 0, int(image_width/3), image_height))
        image_middle = image.crop((int(image_width/3), 0, int(2 * image_width/3), image_height))
        image_right = image.crop((int(2 * image_width/3), 0, image_width, image_height))

        return ComplexKeyboardColorPattern(
            self.get_image_color(image_left), 
            self.get_image_color(image_middle), 
            self.get_image_color(image_right)
        )

    def get_image_color(self, image: _pil_image.Image) -> KeyboardColor:
        image_width, image_height = image.size

        rgb = [0, 0, 0]

        divs = 1
        while image_width * image_height / (divs ** 2) > 10000:
            divs += 1

        n = 0

        for x in range(0, image_width, divs):
            for y in range(0, image_height, divs):
                color: tuple[int, ...] = image.getpixel((x, y)) # type:ignore

                for k in range(3):
                    rgb[k] += color[k]

                n += 1
        
        mini = rgb.index(min(rgb))
        maxi = rgb.index(max(rgb))

        if mini == maxi:
            return KeyboardColor.from_rgb(*[int(i/n) for i in rgb])

        otheri = [i for i in range(3) if not i in [mini, maxi]][0]

        dist = rgb[maxi] - rgb[mini]
        value = (rgb[otheri] - rgb[mini]) / dist

        rgb[mini] = 0
        rgb[otheri] = int(value * 255)
        rgb[maxi] = 255

        return KeyboardColor.from_rgb(*rgb)

    def apply_pattern(self, devices: _T.Sequence[ColoredDevice]) -> None:
        pattern = self.capture_pattern()

        for device in devices:
            device.set_pattern(pattern)
    
    
