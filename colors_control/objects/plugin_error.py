import traceback as _traceback

class PluginError(Exception):
    def __init__(self, file:str, line:int, context:str, content:str, previous_error: 'PluginError | Exception') -> None:
        super().__init__(file, line, context, previous_error)

        self.__file = file
        self.__line = line
        self.__context = context
        self.__content = content
        self.__previous_error = previous_error

    @property
    def file(self) -> str:
        return self.__file
    
    @property
    def context(self) -> str:
        return self.__context
    
    @property
    def content(self) -> str:
        return self.__content
    
    @property
    def line(self) -> int:
        return self.__line
    
    @property
    def previous_error(self) -> 'PluginError | None | Exception':
        return self.__previous_error
    
    def print_traceback(self) -> None:
        print(f"  File {self.__file!r}, line {self.__line}, in {self.__context}")
        print("    " + self.__content)
        print("    " + " " * len("#color-plugin:") + "^" * (len(self.__content) - len("#color-plugin:")))

        if isinstance(self.__previous_error, PluginError):
            self.__previous_error.print_traceback()

        else:
            _traceback.print_tb(self.__previous_error.__traceback__)

            _traceback.print_exception(self.__previous_error)



