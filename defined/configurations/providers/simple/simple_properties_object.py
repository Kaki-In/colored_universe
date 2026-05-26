import typing as _T

from defined.objects import ColorPropertiesObject

class SimplePropertiesObject(_T.TypedDict):
    color: ColorPropertiesObject

    transition_duration_time: int


