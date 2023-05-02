
import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

from models import Join, Ticket, db

from utils import join_us_form



app = Flask("__name__")
app.config.from_object(Config)
db.init_app(app)





@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bize-katil", methods=["POST"])
def join_us():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        education = request.form.get("flexRadioDefault")
        find_where = request.form.get("flexRadioDefault2")
        experince = request.form.get("flexRadioDefault3")
        join_us_form(name=name, email=email, education=education, find_where=find_where, experience=experince)

        return redirect(url_for("index"))


@app.route("/payment/<code>")
def payment(code):
    pass





@app.route("/ticket/<ticketNo>")
def ticket(ticketNo):
    pass

@app.errorhandler(404)
def bad_request(e):
    return render_template("404.html")





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
