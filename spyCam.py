#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  =================================================
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - ven. déc. 14:53 2017
#   - Initial Version 1.0
#  =================================================

from zmqClient import zmqClient
from cameraPipe import cameraPipe

com = zmqClient("meteoCam","tcp://192.168.1.102:5003","tcp://192.168.1.102:5002")
com.start()

cam = cameraPipe("192.168.1.102",5001)

cam.Play()

while (1):
    if com.receiveNb():
        if com.got("ServerUp",True):
            cam.Play()
        if com.got("highRes",True):
            cam.Conf("highRes")
        if com.got("lowRes",True):
            cam.Conf("lowRes")
