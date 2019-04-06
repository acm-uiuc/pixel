from view import view
from config import constants


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
        LOCAL_IMAGE_PATH = "screenImage_" + image_url.split("/")[-1]

        with open(LOCAL_IMAGE_PATH, 'wb') as file:
            file.write(requests.get(image_url).content)

        image = Image.open(LOCAL_IMAGE_PATH).resize(
            (constants.screen_width, constants.screen_height), Image.ANTIALIAS)
        tk_photo_image = ImageTk.PhotoImage(image, master=view.tkapp.w)

        image_location = (constants.screen_width // 2,
                          constants.screen_height // 2)

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
            x * constants.pixel_width,
            y * constants.pixel_height,
            x * constants.pixel_width + constants.pixel_width,
            y * constants.pixel_height + constants.pixel_height,
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
    Custom response for rate limit exceeded
    """

    return make_response("Rate limit exceeded: {}\n".format(e.description), 429)


@blueprint_image.route('/image/screenshot/regular/', methods=['GET'])
def screenshot_regular():
    """
    Return PNG of current canvas, regular size.
    """
    ps = tkapp.w.postscript(colormode='color')
    out = BytesIO()
    Image.open(BytesIO(ps.encode('utf-8'))).save(out, format="PNG")
    out.seek(0)
    return send_file(out, mimetype='image/png')


@blueprint_image.route('/image/screenshot/small/', methods=['GET'])
def screenshot_small():
    """
    Return PNG of current canvas, small size.
    """
    ps = tkapp.w.postscript(colormode='color')
    out = BytesIO()
    im = Image.open(BytesIO(ps.encode('utf-8')))

    im = im.resize((constants.display_width, constants.display_height))
    im.save(out, format="PNG")
    out.seek(0)
    return send_file(out, mimetype='image/png')
