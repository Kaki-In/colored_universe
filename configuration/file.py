import json as _json

import typing as _T
import os as _os

class SettingsFile[DataType]():
    def __init__(self, path:str, default_content: DataType, ext="conf") -> None:
        self._path = path
        self._ext = ext

        if not _os.path.exists(self.get_pathname()):
            self.overwrite(default_content)
    
    def get_pathname(self) -> str:
        return self._path + "." + self._ext

    def get_content(self) -> DataType:
        a = open(self.get_pathname(), "r")
        data = a.read()
        a.close()

        return _json.loads(data)
    
    def overwrite(self, json_content: DataType) -> None:
        a = open(self.get_pathname(), "w")
        a.write(_json.dumps(json_content, indent=4))
        a.close()


