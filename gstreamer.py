#! /usr/bin/python

# pyrtsp - RTSP test server hack
# Copyright (C) 2013  Robert Swain <robert.swain@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import gi
gi.require_version('Gst','1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst, GstVideo, GstRtspServer

Gst.init(None)

mainloop = GObject.MainLoop()

server = GstRtspServer.RTSPServer()

mounts = server.get_mount_points()

factory = GstRtspServer.RTSPMediaFactory()
factory.set_launch('( v4l2src device=/dev/video0 ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! jpegenc ! rtpjpegpay )')

mounts.add_factory("/test", factory)

server.attach(None)

print("stream ready at rtsp://127.0.0.1:8554/test")

mainloop.run()
