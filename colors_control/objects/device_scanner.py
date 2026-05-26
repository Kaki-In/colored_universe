from .device import ColoredDevice

import typing as _T

class DevicesScanner():
    def search_for_devices(self) -> _T.Sequence[ColoredDevice]:
        """
        Search for devices. 

        Implementations of this abstract method should be instant. 
        To allow long-timed scanning, please use threading. 
        """

        raise NotImplementedError("not implemented for " + repr(self))
    

