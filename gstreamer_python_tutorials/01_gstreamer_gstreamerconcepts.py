#!/usr/bin/env python3
import sys
import gi
import logging

gi.require_version("GLib", "2.0")
gi.require_version("GObject", "2.0")
gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib, GObject

logging.basicConfig(level=logging.DEBUG, format="[%(name)s] [%(levelname)8s] - %(message)s")
logger = logging.getLogger(__name__)

# Initialize GStreamer
Gst.init(sys.argv[1:])

# Create the elements
source = Gst.ElementFactory.make("videotestsrc", "source")
filter1 = Gst.ElementFactory.make("vertigotv", "filter1") #vertigo effect
# Videoconvert element is needed because a "negotiation error".
# The sink does not understand what the filter vertigotv is producing due to platform restrictions or available plugins
filter2 = Gst.ElementFactory.make("videoconvert", "filter2")
sink = Gst.ElementFactory.make("autovideosink", "sink")

# Create the empty pipeline
pipeline = Gst.Pipeline.new("test-pipeline")

if not pipeline or not source or not sink or not filter1 or not filter2:
    logger.error("Not all elements could be created.")
    sys.exit(1)

# Build the pipeline
# pipeline = videotestsrc (source) -> autovideosink (sink)
# Example from website uses pipeline.add(source,sink) which leads to an error:
#   Gst.Bin.add() takes exactly 2 arguments (3 given)
# Solution:
pipeline.add(source)
pipeline.add(filter1)
pipeline.add(filter2)
pipeline.add(sink)

# links source to sink
if not source.link(filter1):
    logger.error("Elements could not be linked.")
    sys.exit(1)

if not filter1.link(filter2):
    logger.error("Elements could not be linked.")
    sys.exit(1)

if not filter2.link(sink):
    logger.error("Elements could not be linked.")
    sys.exit(1)

# Modify the source's properties
source.props.pattern = 0
# Can alternatively be done using `source.set_property("pattern",0)`
# or using `Gst.util_set_object_arg(source, "pattern", 0)`

# Start playing
ret = pipeline.set_state(Gst.State.PLAYING)
if ret == Gst.StateChangeReturn.FAILURE:
    logger.error("Unable to set the pipeline to the playing state.")
    sys.exit(1)

# Wait for EOS or error
bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

# Parse error or EOS message
if msg:
    if msg.type == Gst.MessageType.ERROR:
        err, debug_info = msg.parse_error()
        logger.error(f"Error received from element {msg.src.get_name()}: {err.message}")
        logger.error(f"Debugging information: {debug_info if debug_info else 'none'}")
    elif msg.type == Gst.MessageType.EOS:
        logger.info("End-Of-Stream reached.")
    else:
        # This should not happen as we only asked for ERRORs and EOS
        logger.error("Unexpected message received.")

pipeline.set_state(Gst.State.NULL)

