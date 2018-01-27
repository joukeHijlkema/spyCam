#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  =================================================
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - ven. déc. 11:15 2017
#   - Initial Version 1.0
#  =================================================
import sys
sys.path.append("./Classes")

import gi
import time

gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gst
from gi.repository import GLib
from gi.repository import Gtk

Gst.init([])
Gtk.init([])

from videoIn import videoIn
from zmqServer import zmqServer

com = zmqServer("Server","tcp://192.168.1.102:5002","tcp://192.168.1.102:5003")
com.start()

monitor = videoIn(com)

Gtk.main()
