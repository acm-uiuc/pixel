#!/bin/sh
xset s off
xset -dpms
cd /home/pi/pixel
bin/python3 main.py
# export FLASK_APP=pixel.py
# exec python3 -m flask run --host=0.0.0.0
