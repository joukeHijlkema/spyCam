#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  =================================================
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - ven. déc. 15:40 2017
#   - Initial Version 1.0
#  =================================================

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')

from gi.repository import Gst
from gi.repository import GLib

Gst.init([])

import os

class cameraPipe:
    def __init__(self,Host,Port):
        "docstring"
        self.pipe = Gst.Pipeline("pipeline")

        src = Gst.ElementFactory.make("rpicamsrc")
        src.set_property("annotation-mode",12)
        self.pipe.add(src)

        self.t = Gst.ElementFactory.make("tee")
        self.pipe.add(self.t)
        src.link(self.t)

        trans = self.tSink(Host,Port)
        self.pipe.add(trans)
        self.t.link(trans)

        self.rec = self.recLeg("/tmp/spyCam.mp4")
        self.pipe.add(self.rec)
        self.t.link(self.rec)

        bus = self.pipe.get_bus()
        # bus.add_signal_watch()
        # bus.connect("message", self.message)
        bus.set_sync_handler(self.message)
        
        self.Recording = False

    ## --------------------------------------------------------------
    ## Description : start playing
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 29-46-2017 14:46:22
    ## --------------------------------------------------------------
    def Play (self):
        self.pipe.set_state(Gst.State.PLAYING)
        # self.rec.get_by_name("valve").set_property("drop",True)

    ## --------------------------------------------------------------
    ## Description : Conf
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 29-27-2017 15:27:29
    ## --------------------------------------------------------------
    def Conf (self,what):
        print("conf : %s"%what)
        if what == "lowRes":
            self.stopRecording()
        if what == "highRes":
            self.startRecording()

    ## --------------------------------------------------------------
    ## Description : get caps str
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 29-39-2017 15:39:57
    ## --------------------------------------------------------------
    def getCaps (self,args):
        if args=="high":
            return Gst.Caps.from_string("video/x-h264,framerate=25/1,width=1920,height=1080")
        return Gst.Caps.from_string("video/x-h264,framerate=25/1,width=640,height=360")

    ## --------------------------------------------------------------
    ## Description : transmission sink
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 02-11-2018 15:11:30
    ## --------------------------------------------------------------
    def tSink (self,Host,Port):
        bin = Gst.ElementFactory.make('bin')

        q =  Gst.ElementFactory.make("queue")
        bin.add(q)
        
        flt = Gst.ElementFactory.make("capsfilter")
        flt.set_property("caps",self.getCaps("low"))
        bin.add(flt)
        q.link(flt)
                         
        prs = Gst.ElementFactory.make("h264parse")
        bin.add(prs)
        flt.link(prs)

        pay = Gst.ElementFactory.make("rtph264pay")
        pay.set_property("pt",96)
        pay.set_property("config-interval",5)
        bin.add(pay)
        prs.link(pay)

        snk = Gst.ElementFactory.make("udpsink")
        snk.set_property("host",Host)
        snk.set_property("port",Port)
        snk.set_property("sync",False)
        bin.add(snk)
        pay.link(snk)

        gs = Gst.GhostPad('sink', q.get_static_pad('sink'))
        gs.set_active(True)
        bin.add_pad(gs)
        
        return bin

    ## --------------------------------------------------------------
    ## Description :make the recording leg
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 22-09-2017 19:09:48
    ## --------------------------------------------------------------
    def recLeg (self,path):
        bin    = Gst.ElementFactory.make("bin")

        q     = Gst.ElementFactory.make("queue","vQ")
        bin.add(q)

        v = Gst.ElementFactory.make("valve","valve")
        bin.add(v)
        q.link(v)
        
        # flt = Gst.ElementFactory.make("capsfilter")
        # flt.set_property("caps",self.getCaps("high"))
        # bin.add(flt)
        # v.link(flt)

        vParse = Gst.ElementFactory.make("h264parse","vParse")
        bin.add(vParse)
        v.link(vParse)

        vConv = Gst.ElementFactory.make("videoconvert","vConv")
        bin.add(vConv)
        vParse.link(vConv)

        vMux   = Gst.ElementFactory.make("mp4mux","vMux")
        bin.add(vMux)
        vConv.link(vMux)
        
        vOut   = Gst.ElementFactory.make("filesink","vOut")
        vOut.set_property("location",path)
        vOut.set_property("async",0)
        bin.add(vOut)
        vMux.link(vOut)

        # t = Gst.ElementFactory.make("fakesink")
        # bin.add(t)
        # flt.link(t)

        ghostSink = Gst.GhostPad('sink', q.get_static_pad('sink'))
        ghostSink.set_active(True)
        bin.add_pad(ghostSink)

        return bin
    
    ## --------------------------------------------------------------
    ## Description :startRecording
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 02-21-2016 18:21:43
    ## --------------------------------------------------------------
    def startRecording (self):
        print ("start recording : recording = %s"%self.Recording)
        if self.Recording:
            return

        try:
            os.remove("/tmp/spyCam.mp4")
        except OSError:
            print("file does not exist")

        self.rec.get_by_name("valve").set_property("drop",False)

        res = self.pipe.set_state(Gst.State.PLAYING)
        print(res)
        
        if res==Gst.StateChangeReturn.SUCCESS or res==Gst.StateChangeReturn.ASYNC:
            self.Recording = True
            print "Recording"
        else:
            self.Recording = False
            print "NOT recording"
        return self.Recording


    ## --------------------------------------------------------------
    ## Description :stop recording
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 02-28-2016 18:28:53
    ## --------------------------------------------------------------
    def stopRecording (self):
        if not self.Recording:
            return
        print("Stop recording")
        # self.rec.get_by_name("valve").set_property("drop",True)
        self.rec.get_by_name("vOut").get_static_pad("sink").add_probe(Gst.PadProbeType.EVENT_BOTH,self.closeFile,"finalLeg")
        self.rec.get_by_name("vConv").get_static_pad("sink").send_event(Gst.Event.new_eos())

    ## --------------------------------------------------------------
    ## Description :close the file
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 23-53-2017 17:53:32
    ## --------------------------------------------------------------
    def closeFile (self,pad,info,ud):
        print "got %s from %s by %s\n"%(info.get_event().type,ud,pad.get_parent_element().name)
        
        if info.get_event().type==Gst.EventType.EOS:
            print "got %s from %s by %s\n"%(info.get_event().type,ud,pad.get_parent_element().name)
            if ud=="finalLeg":
                print "close all"
                self.Recording = False
                return Gst.PadProbeReturn.REMOVE
            else:
                print "don't know what to do with this\n"
       
            
        return Gst.PadProbeReturn.OK

    ## --------------------------------------------------------------
    ## Description : messages
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 03-21-2018 19:21:32
    ## --------------------------------------------------------------
    def message (self,bus,message):
        who = message.src.name
        msg = message.get_structure().to_string() if message.get_structure() else "None"
        print("%s -> %s"%(who,msg))
        return Gst.BusSyncReply.PASS 
