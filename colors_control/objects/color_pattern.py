from .color import Color

class ColorPattern:
    def __init__(self, *colors: Color) -> None:
        self.__colors = colors

    @property
    def colors(self) -> tuple[Color, ...]:
        return self.__colors

    @property
    def colors_values(self) -> list[int]:
        return [int(i) for i in self.__colors]

    @staticmethod
    def from_values(values: list[int]) -> 'ColorPattern':
        return ColorPattern(*[Color(value) for value in values])
    
    def ensure_pattern_length_compatibility(self, other: 'ColorPattern') -> tuple[list[Color], list[Color]]:
        colors1 = list(self.__colors)
        colors2 = list(other.colors)
        max_len = max(len(colors1), len(colors2))

        if len(colors1) == 1:
            colors1 = [colors1[0]] * len(colors2)

        if len(colors2) == 1:
            colors2 = [colors2[0]] * len(colors1)

        black = Color(0x000000)
        while len(colors1) < max_len:
            colors1.append(black)
        while len(colors2) < max_len:
            colors2.append(black)
        
        return colors1, colors2

    def interpolate_rgb_to(self, other: 'ColorPattern', t: float) -> 'ColorPattern':
        colors1, colors2 = self.ensure_pattern_length_compatibility(other)

        result = [a.interpolate_rgb(b, t) for a, b in zip(colors1, colors2)]
        return ColorPattern(*result)


    def interpolate_hsv_to(self, other: 'ColorPattern', t: float) -> 'ColorPattern':
        colors1, colors2 = self.ensure_pattern_length_compatibility(other)

        result = [a.interpolate_hsv(b, t) for a, b in zip(colors1, colors2)]
        return ColorPattern(*result)
