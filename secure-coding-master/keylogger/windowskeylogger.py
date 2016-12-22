"""
Since different operating systems require different libraries in order
to function properly. This particular module focuses on capturing the
keys that are pressed by a user on a windows machine.
"""

__author__ = "Nathaniel Cotton"
__email__ = "nec2887@rit.edu"

import threading


class WindowsKeyLogger(threading.Thread):
    """
    This keylogger focuses on capturing the keys pressed by a user on a windows
    machine.
    """

    def __init__(self):
        super().__init__()


    def run(self):
        """
        This method will start the execution of the thread, however, this method
        should never be called directly instead the start method should be called.
        This method will start top populate a queue
        :return: None
        """
        pass


    def getQueue(self):
        return []

    def hasInfoToSend(self):
        return False

    def getInfo(self):
        return ''