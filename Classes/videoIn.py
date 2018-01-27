#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  =================================================
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - ven. déc. 11:15 2017
#   - Initial Version 1.0
#  =================================================

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gst
from gi.repository import GLib
from gi.repository import Gtk

from cameraPipe import cameraPipe

class videoIn(Gtk.Window):
    def __init__(self,com):
        "docstring"
        super(videoIn, self).__init__()

        self.com = com
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("Classes/spyCam.glade")

        handlers = {
            "quitButton_clicked_cb": self.Quit,
            "high_clicked_cb": self.High,
            "low_clicked_cb": self.Low,
            "mute_toggled_cb": self.Mute
        }

        self.builder.connect_signals(handlers)
        self.camPipe = cameraPipe(5001)
        self.builder.get_object("box1").add(self.camPipe)
        self.builder.get_object("mainWindow").show_all()
        
    ## --------------------------------------------------------------
    ## Description : Quit
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 25-21-2017 16:21:34
    ## --------------------------------------------------------------
    def Quit (self,args):
        self.camPipe.myAlarm.Running = False
        self.camPipe.myAlarm.event.set()
        Gtk.main_quit()

    ## --------------------------------------------------------------
    ## Description : high resolution
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 29-18-2017 16:18:13
    ## --------------------------------------------------------------
    def High (self,args):
        self.com.send("meteoCam",["highRes"])

    ## --------------------------------------------------------------
    ## Description : low resolution
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 29-18-2017 16:18:13
    ## --------------------------------------------------------------
    def Low (self,args):
        self.com.send("meteoCam",["lowRes"])
    ## --------------------------------------------------------------
    ## Description : Mute toggle
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 01-27-2018 17:27:31
    ## --------------------------------------------------------------
    def Mute (self,args):
        self.camPipe.myAlarm.Mute= args.get_active()
        self.camPipe.myAlarm.event.set()
        

        
