#!/usr/bin/python3

from colors_control.objects import ColoredDevicesManager
from colors_control.configuration import MainConfiguration

from time import *

import sys

def main(args: list[str]):
    configuration = MainConfiguration()
    manager = ColoredDevicesManager(configuration)

    return manager.main()

if __name__ == '__main__':
    sys.exit(main(sys.argv))

