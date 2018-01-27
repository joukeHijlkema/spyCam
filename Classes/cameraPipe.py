#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  =================================================
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - ven. déc. 12:09 2017
#   - Initial Version 1.0
#  =================================================

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gst
from gi.repository import GLib
from gi.repository import Gtk

from Alarm import Alarm

class cameraPipe(Gtk.Box):
    def __init__(self,Port):
        "docstring"
        super(cameraPipe, self).__init__()

        self.pipe = Gst.Pipeline("pipeline")

        src = Gst.ElementFactory.make("udpsrc")
        src.set_property("port",Port)
        src.set_property("caps",Gst.Caps.from_string("application/x-rtp,media=video,payload=96,encoding-name=H264,clock-rate=90000"))
        self.pipe.add(src)

        buf = Gst.ElementFactory.make("rtpjitterbuffer")
        self.pipe.add(buf)
        src.link(buf)

        dep = Gst.ElementFactory.make("rtph264depay")
        self.pipe.add(dep)
        buf.link(dep)

        dec = Gst.ElementFactory.make("avdec_h264")
        self.pipe.add(dec)
        dep.link(dec)

        cnv = Gst.ElementFactory.make("videoconvert")
        self.pipe.add(cnv)
        dec.link(cnv)
        
        flp = Gst.ElementFactory.make("videoflip")
        flp.set_property("method",1)
        self.pipe.add(flp)
        cnv.link(flp)

        mot = Gst.ElementFactory.make("motioncells","motion")
        mot.set_property("sensitivity",0.5)
        self.pipe.add(mot)
        flp.link(mot)
        
        cnv2 = Gst.ElementFactory.make("videoconvert")
        self.pipe.add(cnv2)
        mot.link(cnv2)
        
        out = Gst.ElementFactory.make("gtksink")
        self.pipe.add(out)
        cnv2.link(out)

        out.get_property("widget").set_size_request(360, 640)
        self.add(out.get_property("widget"))

        self.connect("realize",self.realised)

        bus = self.pipe.get_bus()
        # bus.add_signal_watch()
        # bus.connect("message", self.message)
        bus.set_sync_handler(self.message2,None)
        
        self.myAlarm = Alarm()
        self.myAlarm.start()

    ## --------------------------------------------------------------
    ## Description : start camera when widget is realized
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 29-11-2017 12:11:41
    ## --------------------------------------------------------------
    def realised (self,args):
        print("start playing %s"%self.pipe.set_state(Gst.State.PLAYING))

    ## --------------------------------------------------------------
    ## Description : Messages
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 29-25-2017 12:25:38
    ## --------------------------------------------------------------
    def message (self,bus,message):
        who = message.src.name
        msg = message.get_structure() if message.get_structure() else "None"
        print("%s"%who)
        if message.type == Gst.MessageType.STATE_CHANGED:
            print("- %s"%msg.to_string())
    ## --------------------------------------------------------------
    ## Description : msg2
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 29-10-2017 13:10:27
    ## --------------------------------------------------------------
    def message2 (self,bus,msg,usrData):
        who = msg.src.name
        if who =="motion":
            self.motionDetected(msg)
            return Gst.BusSyncReply.DROP
        return Gst.BusSyncReply.PASS

    ## --------------------------------------------------------------
    ## Description : motion detected
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 29-45-2017 14:45:19
    ## -------------------------------------------------------
    def motionDetected (self,msg):
        self.myAlarm.event.set()

