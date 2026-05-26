from .file import SettingsFile

import typing as _T

class SettingsSubFile[FileDataType, ObjectDataType]():
    def __init__(self, file: SettingsFile[FileDataType]) -> None:
        self._file = file

    def get_data(self) -> ObjectDataType:
        return self._get_data_from_file(self._file.get_content())

    def _get_data_from_file(self, file_data: FileDataType) -> ObjectDataType:
        raise NotImplementedError("not implemented for " + repr(self))
    
