import config.constants
import view.screen
import endpoints.commons

import flask

import PIL
import PIL.Image
import PIL.ImageTk

import tkinter as tk

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
@blueprint_image.route('/', methods=['POST'])
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
        return endpoints.commons.construct_response()
    except Exception as e:
        return endpoints.commons.construct_response(status="Failure", message=str(e))


@blueprint_image.errorhandler(429)
def image_ratelimit(e):
    """
    Custom response for rate limit exceeded.
    """

    return flask.make_response("Rate limit exceeded: {}.".format(e.description), 429)


@blueprint_image.route('/screenshot/regular.png/', methods=['GET'])
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


@blueprint_image.route('/screenshot/small.png/', methods=['GET'])
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
