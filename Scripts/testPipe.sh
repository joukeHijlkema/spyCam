#!/bin/bash

gst-launch-1.0 -v rpicamsrc annotation-mode=12 ! \
	       tee name=tee ! \
	       queue ! video/x-h264,framerate=25/1,width=640,height=360 ! \
	       rtph264pay pt=96 config-interval=5 ! \
	       udpsink host=192.168.1.102 port=5001 \
	       tee. ! queue name=filequeue ! \
	       h264parse ! mp4mux ! filesink location=/tmp/test.mp4
