#!/usr/bin/env python3
# Evan Widloski - 2018-10-15
from flask import Flask, request, make_response, redirect, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import tkinter as tk
import threading
from tkinter import *
from PIL import Image
from io import BytesIO

screen_width = 1280
screen_height = 1024
display_width = 128
display_height = 128

pixel_width = screen_width / display_width
pixel_height = screen_height / display_height

logging.basicConfig(level=logging.INFO, format='%(message)s')

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)


class TkApp(threading.Thread):
    """Separate thread for tkinter canvas"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.w = tk.Canvas(self.root, width=screen_width, height=screen_height)
        self.w.pack()

        label = tk.Label(self.root, text="Hello World")
        label.pack()

        self.root.mainloop()


tkapp = TkApp()

# @limiter.limit("2/minute")
@app.route('/', methods=['POST'])
def root():
    """POST endpoint for JSON data"""

    try:
        x = int(request.form.get('x'))
        y = int(request.form.get('y'))
        color = request.form.get('color')

        tkapp.w.create_rectangle(
            x * pixel_width,
            y * pixel_height,
            x * pixel_width + pixel_width,
            y * pixel_height + pixel_height,
            fill=color,
            width=0,
            outline=""
        )
    except Exception:
        return "you suck\n"

    return "success\n"

@app.route('/image.png', methods=['GET'])
def image():
    """Return png of current canvas"""
    ps = tkapp.w.postscript(colormode='color')
    out = BytesIO()
    Image.open(BytesIO(ps.encode('utf-8'))).save(out, format="PNG")
    out.seek(0)
    return send_file(out, mimetype='image/png')

@app.route('/image_small.png', methods=['GET'])
def image_small():
    """Return png of current canvas"""
    ps = tkapp.w.postscript(colormode='color')
    out = BytesIO()
    im = Image.open(BytesIO(ps.encode('utf-8')))
    # im = im.resize((display_width, display_height), Image.ANTIALIAS)
    # im = im.resize((display_width, display_height), resample=Image.BILINEAR)
    im = im.resize((display_width, display_height))
    im.save(out, format="PNG")
    out.seek(0)
    return send_file(out, mimetype='image/png')


@app.route('/', methods=['GET'])
def readme():
    return redirect("https://www.github.com/acm-uiuc/pixel")

@app.errorhandler(429)
def ratelimit(e):
    """Custom response for rate limit exceeded"""

    return make_response("Rate limit exceeded: {}\n".format(e.description), 429)



