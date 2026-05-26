import colorsys

class Color:
    def __init__(self, value: int):
        if not (0x000000 <= value <= 0xFFFFFF):
            raise ValueError("Color value must be between 0x000000 and 0xFFFFFF")
        
        self.__value = value

    @property
    def hex(self) -> str:
        return f"#{self.__value:06X}"

    @property
    def rgb(self) -> tuple[int, int, int]:
        r = (self.__value >> 16) & 0xFF
        g = (self.__value >> 8) & 0xFF
        b = self.__value & 0xFF

        return (r, g, b)

    @property
    def red(self) -> int:
        return (self.__value >> 16) & 0xFF

    @property
    def green(self) -> int:
        return (self.__value >> 8) & 0xFF

    @property
    def blue(self) -> int:
        return self.__value & 0xFF

    @property
    def hsv(self) -> tuple[float, float, float]:
        r, g, b = [x / 255.0 for x in self.rgb]
        return colorsys.rgb_to_hsv(r, g, b)

    @property
    def hue(self) -> float:
        return self.hsv[0]
    
    @property
    def hsv_saturation(self) -> float:
        return self.hsl[2]

    @property
    def value(self) -> float:
        return self.hsv[2]

    @property
    def hsl(self) -> tuple[float, float, float]:
        r, g, b = [x / 255.0 for x in self.rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return h, s, l

    @property
    def lightness(self) -> float:
        return self.hsl[2]

    @property
    def hsl_saturation(self) -> float:
        return self.hsl[1]

    @property
    def cmyk(self) -> tuple[float, float, float, float]:
        r, g, b = self.rgb
        r_prime, g_prime, b_prime = r / 255.0, g / 255.0, b / 255.0

        k = 1 - max(r_prime, g_prime, b_prime)
        if k == 1:
            return (0.0, 0.0, 0.0, 1.0)

        c = (1 - r_prime - k) / (1 - k)
        m = (1 - g_prime - k) / (1 - k)
        y = (1 - b_prime - k) / (1 - k)

        return (c, m, y, k)

    @property
    def cyan(self) -> float:
        return self.cmyk[0]

    @property
    def magenta(self) -> float:
        return self.cmyk[1]

    @property
    def yellow(self) -> float:
        return self.cmyk[2]

    @property
    def black(self) -> float:
        return self.cmyk[3]

    @staticmethod
    def from_rgb(r: int, g: int, b: int) -> 'Color':
        return Color((r << 16) + (g << 8) + b)

    @staticmethod
    def from_hsv(h: float, s: float, v: float) -> 'Color':
        r, g, b = colorsys.hsv_to_rgb(h % 1.0, max(0, min(1, s)), max(0, min(1, v)))
        return Color.from_rgb(int(r * 255), int(g * 255), int(b * 255))

    @staticmethod
    def from_hsl(h: float, s: float, l: float) -> 'Color':
        r, g, b = colorsys.hls_to_rgb(h % 1.0, max(0, min(1, l)), max(0, min(1, s)))
        return Color.from_rgb(int(r * 255), int(g * 255), int(b * 255))

    @staticmethod
    def from_cmyk(c: float, m: float, y: float, k: float) -> 'Color':
        c = max(0.0, min(1.0, c))
        m = max(0.0, min(1.0, m))
        y = max(0.0, min(1.0, y))
        k = max(0.0, min(1.0, k))

        r = int(255 * (1 - c) * (1 - k))
        g = int(255 * (1 - m) * (1 - k))
        b = int(255 * (1 - y) * (1 - k))
        
        return Color.from_rgb(r, g, b)

    def __int__(self) -> int:
        return self.__value

    def __repr__(self) -> str:
        return f"Color({self.hex})"
    
    def __hash__(self) -> int:
        return self.__value
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.__value == other
        
        if isinstance(other, Color):
            return other.__value == self.__value
        
        raise TypeError()

    def __add__(self, other: object) -> 'Color':
        if type(other) is Color:
            return Color.from_rgb(*[min(255, a + b) for a, b in zip(self.rgb, other.rgb)])
        
        raise TypeError()

    def __sub__(self, other: object) -> 'Color':
        if type(other) is Color:
            return Color.from_rgb(*[max(0, a - b) for a, b in zip(self.rgb, other.rgb)])
        
        raise TypeError()

    def rotate_hue(self, degrees: float) -> 'Color':
        h, s, v = self.hsv
        h = (h + degrees / 360.0) % 1.0
        return Color.from_hsv(h, s, v)

    def interpolate_rgb(self, other: 'Color', t: float) -> 'Color':
        if not (0 <= t <= 1):
            raise ValueError("Interpolation factor must be between 0 and 1")
        
        r1, g1, b1 = self.rgb
        r2, g2, b2 = other.rgb

        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        
        return Color.from_rgb(r, g, b)

    def interpolate_hsv(self, other: 'Color', t: float) -> 'Color':
        if not (0.0 <= t <= 1.0):
            raise ValueError("Interpolation factor must be between 0 and 1")

        h1, s1, v1 = self.hsv
        h2, s2, v2 = other.hsv

        dh = (h2 - h1) % 1.0
        if dh > 0.5:
            dh -= 1.0
            
        h = (h1 + dh * t) % 1.0

        s = s1 + (s2 - s1) * t
        v = v1 + (v2 - v1) * t

        return Color.from_hsv(h, s, v)

    def with_red(self, red: int) -> 'Color':
        _, g, b = self.rgb
        return Color.from_rgb(max(0, min(255, red)), g, b)

    def with_green(self, green: int) -> 'Color':
        r, _, b = self.rgb
        return Color.from_rgb(r, max(0, min(255, green)), b)

    def with_blue(self, blue: int) -> 'Color':
        r, g, _ = self.rgb
        return Color.from_rgb(r, g, max(0, min(255, blue)))
    
    def with_cyan(self, cyan: float) -> 'Color':
        _, m, y, k = self.cmyk
        return Color.from_cmyk(cyan, m, y, k)

    def with_magenta(self, magenta: float) -> 'Color':
        c, _, y, k = self.cmyk
        return Color.from_cmyk(c, magenta, y, k)

    def with_yellow(self, yellow: float) -> 'Color':
        c, m, _, k = self.cmyk
        return Color.from_cmyk(c, m, yellow, k)

    def with_black(self, black: float) -> 'Color':
        c, m, y, _ = self.cmyk
        return Color.from_cmyk(c, m, y, black)

    def with_hue(self, hue: float) -> 'Color':
        _, s, v = self.hsv
        return Color.from_hsv(hue % 1.0, s, v)

    def with_hsl_saturation(self, saturation: float) -> 'Color':
        h, _, l = self.hsl
        return Color.from_hsl(h, saturation, l)

    def with_hsv_saturation(self, saturation: float) -> 'Color':
        h, _, v = self.hsv
        return Color.from_hsv(h, saturation, v)

    def with_value(self, value: float) -> 'Color':
        h, s, _ = self.hsv
        return Color.from_hsv(h, s, value)

    def with_lightness(self, lightness: float) -> 'Color':
        h, _, s = self.hsl
        return Color.from_hsl(h, s, lightness)
