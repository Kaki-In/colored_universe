from .device import ColoredDevice

import typing as _T
import abc as _abc

class DevicesScanner(_abc.ABC):
    @_abc.abstractmethod
    def search_for_devices(self) -> _T.Sequence[ColoredDevice]:
        """
        Search for devices. 

        Implementations of this abstract method should be instant. 
        To allow long-timed scanning, please use threading. 
        """
        ...
    

