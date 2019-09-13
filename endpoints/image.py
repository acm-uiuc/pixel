import config.constants
import view.screen
from endpoints.commons import construct_response, write_bmp, create_bmp

import flask

import PIL
import PIL.Image
import PIL.ImageTk
import webcolors

import tkinter as tk

import io
import json
import sys
import cgi
import logging

log = logging.getLogger(__name__)

blueprint_image = flask.Blueprint('blueprint_image', __name__)
create_bmp()

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

        parsed_color = webcolors.html5_parse_legacy_color(color)
        write_bmp(x, y, parsed_color.red, parsed_color.green, parsed_color.blue)

        return construct_response()
    except Exception as e:
        import traceback
        log.error(traceback.format_exc())
        return construct_response(status="Failure", message=str(e))


@blueprint_image.errorhandler(429)
def image_ratelimit(e):
    """
    Custom response for rate limit exceeded.
    """

    return flask.make_response("Rate limit exceeded: {}.".format(e.description), 429)


@blueprint_image.route('/large.bmp', methods=['GET'])
def screenshot_regular():
    """
    Return a large size BMP of the current canvas.
    """
    pass


@blueprint_image.route('/small.bmp', methods=['GET'])
def screenshot_small():
    """
    Returns a small size BMP of the current canvas.
    """

    return flask.send_file('image.bmp')
