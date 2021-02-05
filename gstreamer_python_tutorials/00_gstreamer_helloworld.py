#!/usr/bin/env python3
#credits : https://gstreamer.freedesktop.org/documentation/tutorials/basic/hello-world.html?gi-language=python

import sys
import gi

gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject, GLib

pipeline = None
bus = None
message = None

# initialize GStreamer
Gst.init(sys.argv[1:])

# build the pipeline
# Gst.parse_launch:
pipeline = Gst.parse_launch(
    "playbin uri=https://www.freedesktop.org/software/gstreamer-sdk/data/media/sintel_trailer-480p.webm"
)

# start playing
pipeline.set_state(Gst.State.PLAYING)

## wait until EOS (END OF STREAM) or error
bus = pipeline.get_bus() #retrieves the pipeline's bus
#blocks until EOS or error
msg = bus.timed_pop_filtered(
    Gst.CLOCK_TIME_NONE,
    Gst.MessageType.ERROR | Gst.MessageType.EOS
)

# free resources
pipeline.set_state(Gst.State.NULL)

