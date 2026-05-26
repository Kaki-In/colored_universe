import typing as _T

from defined.objects import NamedColorPropertiesObject, SimpleKeyboardPatternObject, ComplexKeyboardPatternObject

class KeyboardPatternDescription[type_literal: str, PatternType](_T.TypedDict):
    type: type_literal
    pattern: PatternType

class SimplePatternDescription(KeyboardPatternDescription[_T.Literal['simple'], SimpleKeyboardPatternObject]):
    pass

class ComplexPatternDescription(KeyboardPatternDescription[_T.Literal['complex'], ComplexKeyboardPatternObject]):
    pass

class SimpleColorProviderDeviceSavesObject(_T.TypedDict):
    previous_color: SimplePatternDescription | ComplexPatternDescription
    previous_color_time: float

    previous_target_color: str

