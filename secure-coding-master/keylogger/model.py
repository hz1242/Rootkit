"""
This model file contains general utility functions along with model objects to be used
with the keylogger implementations.
"""

__author__ = "Nathaniel Cotton"
__email__ = "nec2887@rit.edu"

import sys


class Key:
    """
    Not used, but the idea is to create a standard model for which the keyloggers of different
    systems would produce.  This would allow for other software to not
    need to be aware of the underlying operating system.
    """
    __slots__ = ['key', 'ctrl', 'shift']

    def __init__(self, key, ctrl, shift):
        self.key = key
        self.ctrl = ctrl
        self.shift = shift


def getKeyLogger():
    """
    A platform independent function that will produce a keylogger that is specific
    to the system in question.
    :return:
    """
    if 'linux' == sys.platform:
        from keylogger.linuxkeylogger import LinuxKeyLogger
        return LinuxKeyLogger()
    elif 'windows' == sys.platform:
        from keylogger.windowskeylogger import WindowsKeyLogger
        return WindowsKeyLogger()

    return None
