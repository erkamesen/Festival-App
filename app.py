
import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config





app = Flask("__name__")
app.config.from_object(Config)
db = SQLAlchemy(app)




@app.route("/")
def index():
    return render_template("index.html")



@app.errorhandler(404)
def bad_request(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
