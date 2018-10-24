#!/bin/sh
export FLASK_APP=pixel.py
cd /home/pi/pixel
exec /home/pi/venv3/bin/python3 -m flask run --host=0.0.0.0
