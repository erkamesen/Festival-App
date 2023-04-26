
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


