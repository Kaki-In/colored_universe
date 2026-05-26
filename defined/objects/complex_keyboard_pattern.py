import typing as _T

from .named_color import NamedColorPropertiesObject

class ComplexKeyboardPatternObject(_T.TypedDict):
    left: NamedColorPropertiesObject
    middle: NamedColorPropertiesObject
    
    right: _T.Optional[NamedColorPropertiesObject]
    logo: _T.Optional[NamedColorPropertiesObject]
    front_left: _T.Optional[NamedColorPropertiesObject]
    front_right: _T.Optional[NamedColorPropertiesObject]
    mouse: _T.Optional[NamedColorPropertiesObject]


