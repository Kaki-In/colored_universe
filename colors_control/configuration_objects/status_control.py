import typing as _T

class StatusControlObject(_T.TypedDict):
    is_running: bool
    required_for_stop: bool

    stopped_error: _T.Optional[str]

