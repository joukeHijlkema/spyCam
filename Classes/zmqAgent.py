#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  =================================================
#  zmqClient.py
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - Initial Version 1.0
#  =================================================
import zmq
import time

class zmqAgent():
    "client for zeromq communication"

    def __init__(self,name):
        
        self.outContext = zmq.Context()
        self.inContext  = zmq.Context()
        
        self.poller     = zmq.Poller()
        self.delimiter  = ":"
        self.Messages   = {}
        self.Age        = {}
        self.maxAge     = 3

        self.name = name
    
    def send(self,Target,Msg,show = True):
        self.outSocket.send_multipart([Target]+Msg)
        if show:
            print("send %s to %s"%(Msg,Target))

    def receiveNb(self):
        socks = dict(self.poller.poll(100))
        if self.inSocket in socks and socks[self.inSocket] == zmq.POLLIN:
            msg = self.inSocket.recv_multipart()
            if msg[0]==self.name or msg[0]=="Global":
                self.storeMsg(msg[1:])
                return True
        return False

    def storeMsg(self,msg):
        key   = msg[0]
        value = msg[1:]
        now = time.time()
        if self.Age.has_key(key) and now-self.Age[key]>self.maxAge:
            self.Messages.pop(key)
            self.Age.pop(key)
        if self.Messages.has_key(key):
            self.Messages[key].append(value)
        else:
            self.Messages[key] = [value]
        self.Age[key]=now
        if not key=="serverStatus":
            print("received %s:%s"%(key,value))

    def got(self,key,erase):
        out = self.Messages.has_key(key)
        if out and erase:
            del self.Messages[key][0]
            if len(self.Messages[key])==0:
                self.Messages.pop(key)
                self.Age.pop(key)
                
            
        return out
    
    def get(self,key,erase):
        out="NotFound"
        if self.Messages.has_key(key):
            out=self.Messages[key][0]
            if erase:
                del self.Messages[key][0]
                if len(self.Messages[key]) ==0:
                    self.Messages.pop(key)
                    self.Age.pop(key)
        return out

    ## --------------------------------------------------------------
    ## Description :get part of a message or none otherwise
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 28-28-2016 20:28:17
    ## --------------------------------------------------------------
    def getPart (self,msg,i):
        if len(msg)>i:
            return msg[i]
        else:
            return None
