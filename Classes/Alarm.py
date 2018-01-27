#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  =================================================
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - lun. janv. 17:19 2018
#   - Initial Version 1.0
#  =================================================

import threading
import subprocess


class Alarm(threading.Thread):
    def __init__(self):
        "docstring"
        threading.Thread.__init__(self)
        self.Mute    = True
        self.event   = threading.Event()
        self.Running = True
        
    ## --------------------------------------------------------------
    ## Description : run
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 01-20-2018 17:20:46
    ## --------------------------------------------------------------
    def run (self):
        while self.Running:
            print 'THREAD: This is the thread speaking, we are Waiting for event to start..'
            event_is_set = self.event.wait()
            self.event.clear()
            if self.Mute:
                print("Alarm")
            else:
                subprocess.call(["/home/hylkema/bin/beep.sh"])

    
