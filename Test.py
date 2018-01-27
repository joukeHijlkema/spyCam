#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  =================================================
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - sam. janv. 17:24 2018
#   - Initial Version 1.0
#  =================================================

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gst
from gi.repository import GLib
from gi.repository import Gtk

src   = Gst.ElementFactory.make("videotestsrc")
camin = Gst.ElementFactory.make("wrappercamerabinsrc")
