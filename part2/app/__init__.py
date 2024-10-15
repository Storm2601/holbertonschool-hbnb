#!/usr/bin/python3

"""Initialize the Flask application."""

from flask import Flask
from flask_restx import Api


def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API')

    # Placeholder for API namespaces (endpoints will be added later)

    return app
