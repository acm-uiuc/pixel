#!/usr/bin/env python3

import flask
import flask_limiter
import logging
import threading
import argparse

# Blueprints
import endpoints
import endpoints.image


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost', help="address to listen on")
    parser.add_argument('--port', type=str, default='8000', help="port to listen on")
    args = parser.parse_args()

    app = flask.Flask(__name__)
    app.register_blueprint(endpoints.image.blueprint_image)

    limiter = flask_limiter.Limiter(
        app, key_func=flask_limiter.util.get_remote_address)

    app.run(args.host, args.port)
