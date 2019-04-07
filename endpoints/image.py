import util.file
import config.constants
import view.screen

import flask

import PIL
import PIL.Image
import PIL.ImageTk

import tkinter as tk
import requests

import io
import json
import sys
import cgi
import logging

blueprint_image = flask.Blueprint('blueprint_image', __name__)


@blueprint_image.route('/', methods=['GET'])
def readme():
    """
    Redirects to GitHub repository.
    """
    return flask.redirect("https://www.github.com/acm-uiuc/pixel")

# @limiter.limit("2/minute")
@blueprint_image.route('/image/link/', methods=['POST'])
def image():
    """
    Upload publicly accessible link of image, and render it on the screen, at full width and height.
    """

    try:
        payload = json.loads(flask.request.data)

        # Extract URL parameter, and sanitize
        image_url = cgi.escape(payload["url"])

        local_image_path = "images/screenImage_" + image_url.split("/")[-1]

        with util.file.safe_open(local_image_path, 'wb') as file:
            downloaded_file_contents = requests.get(image_url).content
            file.write(downloaded_file_contents)

        image = PIL.Image.open(local_image_path).resize(
            (config.constants.SCREEN_WIDTH, config.constants.SCREEN_HEIGHT), PIL.Image.ANTIALIAS)
        tk_photo_image = PIL.ImageTk.PhotoImage(
            image, master=view.screen.tkapp.w)

        image_location = (config.constants.SCREEN_WIDTH // 2,
                          config.constants.SCREEN_HEIGHT // 2)

        view.screen.tkapp.w.create_image(image_location, image=tk_photo_image)

        result = {
            "status": "Success",
            "error": "N/A"
        }
        return json.dumps(result)
    except Exception as e:
        logging.log(logging.FATAL, e)
        result = {
            "status": "Failure",
            "error": str(e)
        }
        return json.dumps(result)

# @limiter.limit("2/minute")
@blueprint_image.route('/image/pixel/', methods=['POST'])
def pixel():
    """
    Send a pixel color, and x and y coordinates to render the pixel.
    """
    try:
        x = int(flask.request.form.get('x'))
        y = int(flask.request.form.get('y'))
        color = flask.request.form.get('color')

        view.screen.tkapp.w.create_rectangle(
            x * config.constants.PIXEL_WIDTH,
            y * config.constants.PIXEL_HEIGHT,
            x * config.constants.PIXEL_WIDTH + config.constants.PIXEL_WIDTH,
            y * config.constants.PIXEL_HEIGHT + config.constants.PIXEL_HEIGHT,
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
            "error": str(e)
        }
        return json.dumps(result)


@blueprint_image.errorhandler(429)
def image_ratelimit(e):
    """
    Custom response for rate limit exceeded.
    """

    return flask.make_response(f"Rate limit exceeded: {e.description}.", 429)


@blueprint_image.route('/image/screenshot/regular/', methods=['GET'])
def screenshot_regular():
    """
    Return a regular size PNG of the current canvas.
    """
    postscript = view.screen.tkapp.w.postscript(colormode='color')
    
    output = io.BytesIO()
    PIL.Image.open(io.BytesIO(postscript.encode('utf-8'))
                   ).save(output, format="PNG")
    output.seek(0)
    
    return flask.send_file(output, mimetype='image/png')


@blueprint_image.route('/image/screenshot/small/', methods=['GET'])
def screenshot_small():
    """
    Returns a small size PNG of the current canvas.
    """
    postscript = view.screen.tkapp.w.postscript(colormode='color')

    output = io.BytesIO()
    image = PIL.Image.open(io.BytesIO(postscript.encode('utf-8')))

    resized_image = image.resize(
        (config.constants.DISPLAY_WIDTH, config.constants.DISPLAY_HEIGHT))

    resized_image.save(output, format="PNG")
    output.seek(0)
    
    return flask.send_file(output, mimetype='image/png')
