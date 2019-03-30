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
# gi.require_version('Gtk', '2.0')

from gi.repository import Gst
# from gi.repository import Gtk

Gst.init([])
# Gtk.init([])

import os
import time

class cameraPipe:
    def __init__(self,Host,Port):
        "docstring"

        self.pipe = Gst.parse_launch("""
        rpicamsrc annotation-mode=12 ! video/x-h264,framerate=25/1,width=640,height=360 ! 
        tee name=tee !    
        queue ! 
        rtph264pay pt=96 config-interval=5 ! 
        udpsink host=%s port=%s """%(Host,Port))

        # self.pipe = Gst.parse_launch("""
        # videotestsrc ! x264enc ! video/x-h264,framerate=25/1,width=640,height=360 !
        # tee name=tee !    
        # queue ! 
        # rtph264pay pt=96 config-interval=5 ! 
        # udpsink host=%s port=%s """%(Host,Port))
        
        bus = self.pipe.get_bus()                            
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

        fileName = "/tmp/spyCam.mp4"

        self.recPipe = Gst.parse_bin_from_description("""queue name=filequeue ! \
        h264parse ! mp4mux ! filesink async=false location=%s"""%fileName,True)

        self.pipe.add(self.recPipe)
        self.pipe.get_by_name("tee").link(self.recPipe)

        res = self.recPipe.set_state(Gst.State.PLAYING)
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
        filequeue = self.recPipe.get_by_name("filequeue")
        filequeue.get_static_pad("src").add_probe(Gst.PadProbeType.BLOCK_DOWNSTREAM, self.probe_block,filequeue)
        print("done")

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
    ## --------------------------------------------------------------
    ## Description : probe block message
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 28-31-2018 11:31:07
    ## --------------------------------------------------------------
    def probe_block(self, pad, buf,fq):
        print("blocked")
        self.pipe.get_by_name("tee").unlink(self.recPipe)
        fq.get_static_pad("sink").send_event(Gst.Event.new_eos())
        print("Stopped recording")
        self.Recording = False
        
        return True
        
