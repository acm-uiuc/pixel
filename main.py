#!/usr/bin/env python3

import flask
import flask_limiter
import logging
import threading

# Blueprints
import endpoints
import endpoints.image


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    app = flask.Flask(__name__)
    app.register_blueprint(endpoints.image.blueprint_image)

    limiter = flask_limiter.Limiter(
        app, key_func=flask_limiter.util.get_remote_address)

    app.run("localhost", "5000")
