#!/usr/bin/env python3

from flask import Flask, request, make_response, send_file, Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import threading

# Blueprints
import endpoints.image


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    app = Flask(__name__)
    app.register_blueprint(endpoints.image.blueprint_image)

    limiter = Limiter(app, key_func=get_remote_address)

    app.run("localhost", "5000")
