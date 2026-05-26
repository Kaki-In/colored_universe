import typing as _T
import traceback as _traceback

class PluginError(Exception):
    def __init__(self, file:str, line:int, context:str, content:str, previous_error: 'PluginError | Exception') -> None:
        super().__init__(file, line, context, previous_error)

        self._file = file
        self._line = line
        self._context = context
        self._content = content
        self._previous_error = previous_error

    def get_file(self) -> str:
        return self._file
    
    def get_context(self) -> str:
        return self._context
    
    def get_content(self) -> str:
        return self._content
    
    def get_line(self) -> int:
        return self._line
    
    def get_previous_error(self) -> 'PluginError | None | Exception':
        return self._previous_error
    
    def print_traceback(self) -> None:
        print(f"  File {self._file!r}, line {self._line}, in {self._context}")
        print("    " + self._content)
        print("    " + " " * len("#color-plugin:") + "^" * (len(self._content) - len("#color-plugin:")))

        if isinstance(self._previous_error, PluginError):
            self._previous_error.print_traceback()

        else:
            _traceback.print_tb(self._previous_error.__traceback__)

            _traceback.print_exception(self._previous_error)



