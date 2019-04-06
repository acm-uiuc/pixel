from view import view
from config import constants
from util import util


from flask import Flask, Blueprint, render_template, session, abort, redirect, request, make_response, send_file, g
import requests
from io import BytesIO
import json
from PIL import Image, ImageTk
import tkinter as tk
import sys

blueprint_image = Blueprint('blueprint_image', __name__)
tkapp = view.tkapp


@blueprint_image.route('/', methods=['GET'])
def readme():
    """
    Redirects to GitHub repository.
    """
    return redirect("https://www.github.com/acm-uiuc/pixel")

# @limiter.limit("2/minute")
@blueprint_image.route('/image/link/', methods=['POST'])
def image():
    """
    Upload publicly accessible link of image, and render it on the screen, at full width and height.
    """

    try:
        payload = json.loads(request.data)
        image_url = payload["url"]
        local_image_path = "images/screenImage_" + image_url.split("/")[-1]

        with util.safe_open(local_image_path, 'wb') as file:
            downloaded_file_contents = requests.get(image_url).content
            file.write(downloaded_file_contents)

        image = Image.open(local_image_path).resize(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), Image.ANTIALIAS)
        tk_photo_image = ImageTk.PhotoImage(image, master=tkapp.w)

        image_location = (constants.SCREEN_WIDTH // 2,
                          constants.SCREEN_HEIGHT // 2)

        tkapp.w.create_image(image_location, image=tk_photo_image)

        result = {
            "status": "Success",
            "error": "N/A"
        }
        return json.dumps(result)
    except Exception as e:
        result = {
            "status": "Failure",
            "error": e
        }
        return json.dumps(result)

# @limiter.limit("2/minute")
@blueprint_image.route('/image/pixel/', methods=['POST'])
def pixel():
    """
    Send a pixel color, and x and y coordinates to render the pixel.
    """
    try:
        x = int(request.form.get('x'))
        y = int(request.form.get('y'))
        color = request.form.get('color')

        tkapp.w.create_rectangle(
            x * constants.PIXEL_WIDTH,
            y * constants.PIXEL_HEIGHT,
            x * constants.PIXEL_WIDTH + constants.PIXEL_WIDTH,
            y * constants.PIXEL_HEIGHT + constants.PIXEL_HEIGHT,
            fill=color,
            width=0,
            outline=""
        )
        result = {
            "status": "Success",
            "error": "N/A"
        }
        return json.dumps(result)
    except Exception as e:
        result = {
            "status": "Failure",
            "error": e
        }
        return json.dumps(result)


@blueprint_image.errorhandler(429)
def image_ratelimit(e):
    """
    Custom response for rate limit exceeded.
    """

    return make_response(f"Rate limit exceeded: {e.description}.", 429)


@blueprint_image.route('/image/screenshot/regular/', methods=['GET'])
def screenshot_regular():
    """
    Return a regular size PNG of the current canvas.
    """
    ps = tkapp.w.postscript(colormode='color')
    out = BytesIO()
    Image.open(BytesIO(ps.encode('utf-8'))).save(out, format="PNG")
    out.seek(0)
    return send_file(out, mimetype='image/png')


@blueprint_image.route('/image/screenshot/small/', methods=['GET'])
def screenshot_small():
    """
    Returns a small size PNG of the current canvas.
    """
    ps = tkapp.w.postscript(colormode='color')
    out = BytesIO()
    im = Image.open(BytesIO(ps.encode('utf-8')))

    im = im.resize((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT))
    im.save(out, format="PNG")
    out.seek(0)
    return send_file(out, mimetype='image/png')
