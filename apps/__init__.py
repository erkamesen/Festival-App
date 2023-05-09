from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session, current_app
from apps.models import db
from apps.views import ticket, payment, home

import requests
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler


def create_app(config):
    app = Flask("__name__", static_folder="./apps/static")
    app.config.from_object(config)
    db.init_app(app)

    app.register_blueprint(home)
    app.register_blueprint(payment)
    app.register_blueprint(ticket)

    register_errorhandlers(app)
    configure_logging(app)

    return app



def configure_logging(app):

    # Deactivate the default flask logger so that log messages don't get duplicated 
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler('./logs/app.log', maxBytes=16384, backupCount=20)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)



def register_errorhandlers(app):
    """Register error handlers with the Flask application."""

    def render_error(e):
        return render_template('%s.html' % e.code), e.code

    for e in [
        requests.codes.INTERNAL_SERVER_ERROR,
        requests.codes.NOT_FOUND,
        requests.codes.UNAUTHORIZED,
    ]:
        app.errorhandler(e)(render_error)