Secure Coding

Author(s):  Nathaniel Cotton

Description:

This project is looking at creating a rootkit that is capable of recording
the keys that a user hits. It will also include functionality for sending
data across a network so that another computer can record the keys that
are being pressed. Additionally, this network functionality will be used
to receive information that can dictate what commands should be executed.
Those commands results can then be sent back to the calling computer, this
allows for a networked rootkit.

Getting Started:

There are three main files that can be used to setup this project, the
first is to run either of the installation scripts (i.e. bat, sh files),
or the rootkit.py file can be executed.

PLEASE DO NOT RUN ANY OF THESE FILES IF YOU DO NOT KNOW WHAT YOU ARE
DOING AS DIFFICULTIES COULD ENSUE.

The installation scripts will copy files and setup the computer to run
to rootkit automatically.


Structure:

rootkit.py                       : entry point
server.py                        : server for communicating with the client
install.bat                      : windows installation
install.sh                       : linux installation
network/
     network.py                  : network functionality
keylogger/
     linuxkeylogger.py           : keylogger for linux systems
     windowskeylogger.py         : keylogger for windows systems
     model.py                    : standard model for all systems

