import colorsys

class Color:
    def __init__(self, value: int):
        if not (0x000000 <= value <= 0xFFFFFF):
            raise ValueError("Color value must be between 0x000000 and 0xFFFFFF")
        
        self._value = value

    def get_hex(self) -> str:
        return f"#{self._value:06X}"

    def get_rgb(self) -> tuple[int, int, int]:
        r = (self._value >> 16) & 0xFF
        g = (self._value >> 8) & 0xFF
        b = self._value & 0xFF

        return (r, g, b)

    def get_red(self) -> int:
        return (self._value >> 16) & 0xFF

    def get_green(self) -> int:
        return (self._value >> 8) & 0xFF

    def get_blue(self) -> int:
        return self._value & 0xFF

    def get_hsv(self) -> tuple[float, float, float]:
        r, g, b = [x / 255.0 for x in self.get_rgb()]
        return colorsys.rgb_to_hsv(r, g, b)

    def get_hue(self) -> float:
        return self.get_hsv()[0]
    
    def get_hsv_saturation(self) -> float:
        return self.get_hsl()[2]

    def get_value(self) -> float:
        return self.get_hsv()[2]

    def get_hsl(self) -> tuple[float, float, float]:
        r, g, b = [x / 255.0 for x in self.get_rgb()]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return h, s, l

    def get_lightness(self) -> float:
        return self.get_hsl()[1]

    def get_hsl_saturation(self) -> float:
        return self.get_hsl()[1]

    def get_cmyk(self) -> tuple[float, float, float, float]:
        r, g, b = self.get_rgb()
        r_prime, g_prime, b_prime = r / 255.0, g / 255.0, b / 255.0

        k = 1 - max(r_prime, g_prime, b_prime)
        if k == 1:
            return (0.0, 0.0, 0.0, 1.0)

        c = (1 - r_prime - k) / (1 - k)
        m = (1 - g_prime - k) / (1 - k)
        y = (1 - b_prime - k) / (1 - k)

        return (c, m, y, k)

    def get_cyan(self) -> float:
        return self.get_cmyk()[0]

    def get_magenta(self) -> float:
        return self.get_cmyk()[1]

    def get_yellow(self) -> float:
        return self.get_cmyk()[2]

    def get_black(self) -> float:
        return self.get_cmyk()[3]

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
        return self._value

    def __repr__(self) -> str:
        return f"Color({self.get_hex()})"
    
    def __hash__(self) -> int:
        return self._value
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self._value == other
        
        if isinstance(other, Color):
            return other._value == self._value
        
        raise TypeError()

    def __add__(self, other: object) -> 'Color':
        if type(other) is Color:
            return Color.from_rgb(*[min(255, a + b) for a, b in zip(self.get_rgb(), other.get_rgb())])
        
        raise TypeError()

    def __sub__(self, other: object) -> 'Color':
        if type(other) is Color:
            return Color.from_rgb(*[max(0, a - b) for a, b in zip(self.get_rgb(), other.get_rgb())])
        
        raise TypeError()

    def rotate_hue(self, degrees: float) -> 'Color':
        h, s, v = self.get_hsv()
        h = (h + degrees / 360.0) % 1.0
        return Color.from_hsv(h, s, v)

    def interpolate_rgb(self, other: 'Color', t: float) -> 'Color':
        if not (0 <= t <= 1):
            raise ValueError("Interpolation factor must be between 0 and 1")
        
        r1, g1, b1 = self.get_rgb()
        r2, g2, b2 = other.get_rgb()

        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        
        return Color.from_rgb(r, g, b)

    def interpolate_hsv(self, other: 'Color', t: float) -> 'Color':
        if not (0.0 <= t <= 1.0):
            raise ValueError("Interpolation factor must be between 0 and 1")

        h1, s1, v1 = self.get_hsv()
        h2, s2, v2 = other.get_hsv()

        dh = (h2 - h1) % 1.0
        if dh > 0.5:
            dh -= 1.0
            
        h = (h1 + dh * t) % 1.0

        s = s1 + (s2 - s1) * t
        v = v1 + (v2 - v1) * t

        return Color.from_hsv(h, s, v)

    def with_red(self, red: int) -> 'Color':
        _, g, b = self.get_rgb()
        return Color.from_rgb(max(0, min(255, red)), g, b)

    def with_green(self, green: int) -> 'Color':
        r, _, b = self.get_rgb()
        return Color.from_rgb(r, max(0, min(255, green)), b)

    def with_blue(self, blue: int) -> 'Color':
        r, g, _ = self.get_rgb()
        return Color.from_rgb(r, g, max(0, min(255, blue)))
    
    def with_cyan(self, cyan: float) -> 'Color':
        _, m, y, k = self.get_cmyk()
        return Color.from_cmyk(cyan, m, y, k)

    def with_magenta(self, magenta: float) -> 'Color':
        c, _, y, k = self.get_cmyk()
        return Color.from_cmyk(c, magenta, y, k)

    def with_yellow(self, yellow: float) -> 'Color':
        c, m, _, k = self.get_cmyk()
        return Color.from_cmyk(c, m, yellow, k)

    def with_black(self, black: float) -> 'Color':
        c, m, y, _ = self.get_cmyk()
        return Color.from_cmyk(c, m, y, black)

    def with_hue(self, hue: float) -> 'Color':
        _, s, v = self.get_hsv()
        return Color.from_hsv(hue % 1.0, s, v)

    def with_hsl_saturation(self, saturation: float) -> 'Color':
        h, _, l = self.get_hsl()
        return Color.from_hsl(h, saturation, l)

    def with_hsv_saturation(self, saturation: float) -> 'Color':
        h, _, v = self.get_hsv()
        return Color.from_hsv(h, saturation, v)

    def with_value(self, value: float) -> 'Color':
        h, s, _ = self.get_hsv()
        return Color.from_hsv(h, s, value)

    def with_lightness(self, lightness: float) -> 'Color':
        h, _, s = self.get_hsl()
        return Color.from_hsl(h, s, lightness)
