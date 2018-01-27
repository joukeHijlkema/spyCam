#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  =================================================
# zmqServer
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - Thu Oct 27 18:01:22 2016
#   - Initial Version 1.0
#  =================================================
import zmq
from zmqAgent import zmqAgent
import time
import threading

class zmqServer(zmqAgent,threading.Thread):
    "zmq server"

    def __init__(self,name,adIn,adOut):
        threading.Thread.__init__(self)
        self.name  = name
        self.adIn  = adIn
        self.adOut = adOut
        
    ## --------------------------------------------------------------
    ## Description :run this thread
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 28-57-2016 13:57:57
    ## --------------------------------------------------------------
    def run(self):
        zmqAgent.__init__(self,self.name)
        self.outSocket  = self.outContext.socket(zmq.PUB)
        self.inSocket   = self.inContext.socket(zmq.PULL)

        self.inSocket.bind(self.adIn)
        print("In  connected to PULL %s"%self.adIn)
        self.outSocket.bind(self.adOut)
        print("Out connected to PUB %s"%self.adOut)
        self.poller.register(self.inSocket, zmq.POLLIN)

        time.sleep(2) ## to make sure all is connected before sending
        self.send("Global",["ServerUp"])

        print ("zmq client running")
