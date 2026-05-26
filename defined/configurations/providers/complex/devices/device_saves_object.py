import typing as _T

from defined.objects import NamedColorPropertiesObject, SimpleKeyboardPatternObject, ComplexKeyboardPatternObject

class KeyboardPatternDescription[type_literal: str, PatternType](_T.TypedDict):
    type: type_literal
    pattern: PatternType

class SimplePatternDescription(KeyboardPatternDescription[_T.Literal['simple'], SimpleKeyboardPatternObject]):
    pass

class ComplexPatternDescription(KeyboardPatternDescription[_T.Literal['complex'], ComplexKeyboardPatternObject]):
    pass

class ComplexColorProviderDeviceSavesObject(_T.TypedDict):
    previous_pattern: SimplePatternDescription | ComplexPatternDescription
    previous_pattern_time: float

    previous_target_pattern: list[str | None]

