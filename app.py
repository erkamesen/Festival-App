from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from config import Config
from models.models import db
from views import ticket, payment, home

def create_app():
    app = Flask("__name__")
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(home)
    app.register_blueprint(payment)
    app.register_blueprint(ticket)
    @app.errorhandler(404)
    def bad_request(e):
        return render_template("404.html")
    
    return app


