#!/usr/bin/env python3
#credits : https://gstreamer.freedesktop.org/documentation/tutorials/basic/hello-world.html?gi-language=python
import logging
import sys
import gi

gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject, GLib

logging.basicConfig(level=logging.INFO, format="[%(name)s] [%(levelname)8s] - %(message)s")

pipeline = None
bus = None
message = None

# initialize GStreamer
Gst.init(sys.argv[1:])

# build the pipeline
# Gst.parse_launch:
pipeline = Gst.parse_launch(
    "v4l2src device=/dev/video0 ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host=192.168.1.23"
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

