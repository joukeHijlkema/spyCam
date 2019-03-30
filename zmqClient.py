#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  =================================================
# zmqClient
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - Thu Oct 27 18:08:55 2016
#   - Initial Version 1.0
#  =================================================

import zmq
from zmqAgent import zmqAgent
import time
import threading

class zmqClient(zmqAgent,threading.Thread):
    "zmq client"
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
        
        self.outSocket  = self.outContext.socket(zmq.PUSH)
        self.inSocket   = self.inContext.socket(zmq.SUB)

        self.inSocket.connect(self.adIn)
        print ("In  connected to PULL %s"%self.adIn)
        self.outSocket.connect(self.adOut)
        print ("Out connected to PUB %s"%self.adOut)
        self.poller.register(self.inSocket, zmq.POLLIN)
        self.subscribe("Global")
        self.subscribe(self.name)

        time.sleep(2) ## to make sure all is connected before sending
        self.send("Server",["CamReady","meteoCam","5001"])

        print ("zmq client running")

    ## --------------------------------------------------------------
    ## Description :subscribe to an extra channel
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 27-19-2016 18:19:25
    ## --------------------------------------------------------------
    def subscribe (self,channel):
        self.inSocket.setsockopt(zmq.SUBSCRIBE, channel)
        print(" - subscribed to %s"%channel)
        
                
