#!/bin/bash
sudo apt-get install python3-pip
sudo pip3 install python-xlib

zip -r kit.zip *
echo '#!/usr/bin/env python3' | cat - kit.zip > kit
chmod +x kit
